from difflib import SequenceMatcher
import re

from tasks.models import CorrectSeg

class OCRCompare(object):
    '''
    用于文字校对前的文本比对，OCR文本除文本外，只含有p或\n
    '''
    @classmethod
    def insert(cls, result_lst, t):
        if t:
            result_lst.append(t)

    @classmethod
    def split_text_by_linefeed(cls, result_lst, text):
        segs = text.split('\n')
        i = 0
        count = len(segs)
        while i < count:
            cls.insert(result_lst, segs[i])
            if i < count - 1:
                result_lst.append('\n')
            i += 1

    @classmethod
    def split_text_by_b(cls, result_lst, text):
        segs = text.split('b')
        i = 0
        count = len(segs)
        while i < count:
            cls.split_text_by_linefeed(result_lst, segs[i])
            if i < count - 1:
                result_lst.append('b')
            i += 1

    @classmethod
    def split_text(cls, text):
        result_lst = []
        segs = text.split('p')
        i = 0
        count = len(segs)
        while i < count:
            cls.split_text_by_b(result_lst, segs[i])
            if i < count - 1:
                result_lst.append('p')
            i += 1
        return result_lst

    @classmethod
    def count_page_line(cls, text, page_no, line_no, char_no):
        for ch in text:
            if ch == 'p':
                page_no += 1
                line_no = 0
                char_no = 0
            elif ch == '\n':
                line_no += 1
                char_no = 1
            elif ch == 'b':
                line_no -= 1
            else:
                char_no += 1
        return (page_no, line_no, char_no)

    @classmethod
    def get_tag(cls, text):
        if text == 'p':
            return CorrectSeg.TAG_P
        elif text == 'b':
            return CorrectSeg.TAG_P
        elif text == '\n':
            return CorrectSeg.TAG_LINEFEED
        return CorrectSeg.TAG_DIFF

    @classmethod
    def generate_compare_reel(cls, text1, text2):
        """
        用于文字校对前的文本比对
        text1是基础本；text2是要比对的版本。
        """
        SEPARATORS_PATTERN = re.compile('[pb\n]')
        text1 = SEPARATORS_PATTERN.sub('', text1)
        correctsegs = []
        pos = 0
        page_no = 0
        line_no = 0
        char_no = 0
        opcodes = SequenceMatcher(lambda x: x in 'pb\n', text1, text2, False).get_opcodes()
        for tag, i1, i2, j1, j2 in opcodes:
            if ((i2-i1) - (j2-j1) > 30):
                base_text = ''
            else:
                base_text = text1[i1:i2]
            if tag == 'equal':
                correctseg = CorrectSeg(tag=CorrectSeg.TAG_EQUAL, position=pos, \
                text1='', text2=text1[i1:i2], selected_text=text1[i1:i2], \
                page_no=page_no, line_no=line_no, char_no=char_no)
                correctsegs.append(correctseg)
                pos += (j2 - j1)
                page_no, line_no, char_no = cls.count_page_line(text2[j1:j2], page_no, line_no, char_no)
            elif tag == 'insert':
                base_text = ''
                result_lst = cls.split_text(text2[j1:j2])
                for result in result_lst:
                    tag = cls.get_tag(result)
                    correctseg = CorrectSeg(tag=tag, position=pos, \
                    text1='', text2=result, selected_text=result, \
                    page_no=page_no, line_no=line_no, char_no=char_no)
                    correctsegs.append(correctseg)
                    pos += len(result)
                    page_no, line_no, char_no = cls.count_page_line(result, page_no, line_no, char_no)
            elif tag == 'replace':
                result_lst = cls.split_text(text2[j1:j2])
                replace_not_inserted = True # 有一次replace
                for result in result_lst:
                    if result not in 'p\n' and replace_not_inserted:
                        correctseg = CorrectSeg(tag=CorrectSeg.TAG_DIFF, position=pos, \
                        text1=base_text, text2=result, selected_text=result, \
                        page_no=page_no, line_no=line_no, char_no=char_no)
                        replace_not_inserted = False
                    else:
                        tag = cls.get_tag(result)
                        correctseg = CorrectSeg(tag=tag, position=pos, \
                        text1='', text2=result, selected_text=result, \
                        page_no=page_no, line_no=line_no, char_no=char_no)
                    correctsegs.append(correctseg)
                    pos += len(result)
                    page_no, line_no, char_no = cls.count_page_line(result, page_no, line_no, char_no)
            elif tag == 'delete':
                correctseg = CorrectSeg(tag=CorrectSeg.TAG_DIFF, position=pos, \
                text1=base_text, text2='', selected_text='', \
                page_no=page_no, line_no=line_no, char_no=char_no)
                correctsegs.append(correctseg)
        return correctsegs