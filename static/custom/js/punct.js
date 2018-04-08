function clean_linefeed(puncts) {
    for (var i = 0; i < puncts.length; ++i) {
        var punct_lst = [];
        for (var j = 0; j < puncts[i].length; ++j) {
            var pos = puncts[i][j][0];
            var ch = puncts[i][j][1];
            if (ch != '\n') {
                punct_lst.push([pos, ch]);
            }
        }
        puncts[i] = punct_lst;
    }
}

function merge_text_punct(text, puncts, punct_result) {
    //clean_linefeed(puncts);
    var TYPE_TEXT = 1;
    var TYPE_SEP = 2;
    var TYPE_BR = 3;

    var result_idx = 0;
    var result_len = punct_result.length;

    var punctseg_lst = [];
    var indexs = [];
    for (var i = 0; i < puncts.length; ++i) {
        indexs.push(0);
    }
    var text_idx = 0;
    while (1) {
        // 找到当前最小的punct位置
        var min_pos = text.length;
        var min_punct_index = -1;
        for (var i = 0; i < puncts.length; ++i) {
            var index = indexs[i];
            if (index < puncts[i].length) {
                var punct_obj = puncts[i][index];
                if (punct_obj[0] < min_pos) {
                    min_pos = punct_obj[0];
                    min_punct_index = i;
                }
            }
        }

        if (text_idx < min_pos) {
            var text_seg = text.substr(text_idx, min_pos - text_idx);
            var user_puncts = [];
            var strs = [];
            var t_idx = 0;
            while (result_idx < result_len && 
                (punct_result[result_idx][0] < min_pos ||
                    (punct_result[result_idx][0] == min_pos && punct_result[result_idx][1] != '\n'))) {
                if (punct_result[result_idx][0] - text_idx > t_idx) {
                    var s = text_seg.substr(t_idx, punct_result[result_idx][0] - text_idx - t_idx);
                    strs.push(s);
                    t_idx = punct_result[result_idx][0] - text_idx;
                }

                strs.push(punct_result[result_idx][1]);
                user_puncts.push(punct_result[result_idx]);
                ++result_idx;
            }
            if (t_idx < text_seg.length) {
                var s = text_seg.substr(t_idx, text_seg.length - t_idx);
                strs.push(s);
            }
            text_seg = strs.join('');
            var punctseg = {
                type: TYPE_TEXT,
                position: text_idx,
                text: text_seg, // 经文或合并的标点
                cls: '', // 显示标点的样式
                user_puncts: user_puncts
            };
            punctseg_lst.push(punctseg);
            text_idx = min_pos;
        }

        // 插入标点
        if (min_punct_index != -1) {
            var index = indexs[min_punct_index];
            var cls = 'punct' + (min_punct_index + 1).toString();
            var punct_obj = puncts[min_punct_index][index];
            var punct_str = punct_obj[1];
            var punctseg = {
                type: TYPE_SEP,
                position: text_idx,
                text: punct_obj[1], // 经文或合并的标点
                cls: cls, // 显示标点
                user_puncts: []
            };
            punctseg_lst.push(punctseg);
            indexs[min_punct_index] += 1;
        } else {
            if (text_idx == text.length) {
                break;
            }
        }
    }

    return punctseg_lst;
}

var PUNCT_LIST = '：，。；、！？‘’”“\n';
Vue.component('punct-show-seg', {
    props: ['punctseg', 'sharedata'],
    template: '\
      <span v-if="punctseg.type == 1" contenteditable="true" @input.stop.prevent="inputHandler" v-html="merged_html"></span>\
      <span v-else-if="punctseg.type == 2 && sharedata.show_refpunct" v-bind:class="punctseg.cls">{{ punctseg.text }}</span>\
      <span v-else-if="punctseg.type == 3 && sharedata.show_refpunct"><br /></span>\
    ',
    data: function() {
        return {
            merged_html: ''
        }
    },
    created: function() {
        this.createMergedHtml();
    },
    methods: {
        cleanPunct: function(str) {
            var ch_lst = [];
            for (var i = 0; i < str.length; ++i) {
              if (PUNCT_LIST.indexOf(str[i]) == -1) {
                ch_lst.push(str[i]);
              }
            }
            return ch_lst.join('');
        },
        createMergedHtml: function() {
            if (this.punctseg.type == 1) {
                var html_lst = [];
                var punct_idx = 0;
                var offset = 0;
                while (true) {
                    var offset_n = this.punctseg.text.length;
                    if (punct_idx < this.punctseg.user_puncts.length) {
                        offset_n = this.punctseg.user_puncts[punct_idx][0] - this.punctseg.position;
                    }
                    if (offset == offset_n) {
                        break;
                    }
                    var text = this.punctseg.text.substr(offset, offset_n - offset);
                    html_lst.push('<span class="puncttext">' + text + '</span>');
                    offset = offset_n;
                    var punct_seg = [];
                    while (punct_idx < this.punctseg.user_puncts.length
                        && offset == (this.punctseg.user_puncts[punct_idx][0] - this.punctseg.position)) {
                        var punct_ch = this.punctseg.user_puncts[punct_idx][1];
                        if (punct_ch == '\n') {
                            punct_seg.push('<br />');
                        } else {
                            punct_seg.push(punct_ch);
                        }
                        punct_idx++;
                    }
                    if (punct_seg.length > 0) {
                        html_lst.push('<span class="userpunct">' + punct_seg.join('') + '</span>');
                    }
                }
                this.merged_html = html_lst.join('');
            }
        },
        getNodeIndex: function (node) {
            var n = 0;
            while (node = node.previousSibling) {
                n++;
            }
            return n;
        },
        inputHandler: function(e) {
            var selection = window.getSelection();
            var cursor_offset = selection.focusOffset;
            var focusNode = selection.focusNode;
            var parentNode = focusNode.parentNode;
            var parentNodeIndex = this.getNodeIndex(parentNode);
            // console.log('cursor_offset: ', cursor_offset);
            // console.log('focusNode: ', focusNode);
            // console.log('parent: ', parentNode, parentNodeIndex, e.target);

            var newtext = e.target.innerText;
            
            if (this.cleanPunct(newtext) == this.cleanPunct(this.punctseg.text)) {
                var new_user_puncts = [];
                var offset = 0;
                for (var i = 0; i < newtext.length; ++i) {
                    if (PUNCT_LIST.indexOf(newtext[i]) != -1) {
                        var pos = this.punctseg.position + offset;
                        new_user_puncts.push([pos, newtext[i]]);
                    } else {
                        ++offset;
                    }
                }
                this.punctseg.user_puncts = new_user_puncts;
                this.createMergedHtml();
                // set cursor position
                this.$nextTick(function(){
                    var offset = cursor_offset;
                    parentNode = e.target.childNodes[parentNodeIndex];
                    focusNode = parentNode.firstChild;
                    while (focusNode.length < offset) {
                        offset = offset - focusNode.length;
                        parentNode = parentNode.nextSibling;
                        focusNode = parentNode.firstChild;
                    }
                    var range = document.createRange();
                    range.selectNode(focusNode);
                    range.setStart(focusNode, offset);
                    range.collapse(true);
                    e.target.focus();
                    selection = window.getSelection();
                    selection.removeAllRanges();
                    selection.addRange(range);
                 });
            } else {
                e.target.innerHTML = this.merged_html;
                this.$nextTick(function(){
                    parentNode = e.target.childNodes[parentNodeIndex];
                    focusNode = parentNode.firstChild;
                    var range = document.createRange();
                    range.selectNode(focusNode);
                    var offset = cursor_offset - 1;
                    if (e.isComposing) {
                        offset = cursor_offset;
                    }
                    range.setStart(focusNode, offset);
                    range.collapse(true);
                    e.target.focus();
                    selection = window.getSelection();
                    selection.removeAllRanges();
                    selection.addRange(range); 
                });
            }
        }
    }
});