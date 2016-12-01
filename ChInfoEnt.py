#-*-encoding:utf-8-*-

import sys
import math
reload(sys)
sys.setdefaultencoding("utf-8")

class ChInfoEnt:
    def __init__(self):
        self.version = None
        self.totalDf = None
        self.dfMap = {}

    def SplitterCh_Utf8(self,str_txt):
        uni_str = unicode(str_txt, "utf-8")
        slen = len(uni_str)

        uni_ch_str = ""
        for i in range(slen):
            uchar = uni_str[i]
            if uchar >= u'\u4e00' and uchar<= u'\u9fa5':
                uni_ch_str += uchar
            elif (uchar == u'\u0040' or uchar == u'\u002d' or uchar == u'\u005f' or uchar == u'\u300a' or uchar == u'\u300b') :
                uni_ch_str += uchar
            elif uchar >= u'\u0030' and uchar<=u'\u0039':
                uni_ch_str += uchar
            else:
                pass

        utf8_str = uni_ch_str.encode("utf-8")
        return utf8_str

    def SpliterEn_Utf8(self,str_txt):
        uni_str = unicode(str_txt, "utf-8")
        slen = len(uni_str)

        uni_ch_str = ""
        for i in range(slen):
            uchar = uni_str[i]
            if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
                if uchar >= u'\u0041' and uchar <= u'\u005a':
                    uni_ch_str += uchar.lower()
                else:
                    uni_ch_str += uchar
            elif (
                                uchar == u'\u0040' or uchar == u'\u002d' or uchar == u'\u005f' or uchar == u'\u300a' or uchar == u'\u300b'):
                uni_ch_str += uchar
            elif uchar >= u'\u0030' and uchar <= u'\u0039':
                uni_ch_str += uchar
            else:
                pass

            utf8_str = uni_ch_str.encode("utf-8")
            return utf8_str

        def LoadChDfStat(self, dfFile):
            for line in open(dfFile):
                if not line:
                    continue

                if not self.version:
                    subStr = line.strip().split(":")
                    if subStr[0] != "Version":
                        break
                    else:
                        self.version = subStr[1]
                    continue

                if not self.totalDf:
                    subStr = line.strip().split(":")
                    if subStr[0] != "TOTAL_DF":
                        break
                    else:
                        self.totalDf = int(subStr[1])
                    continue

                subStr = line.strip().split(":")
                word = subStr[0].decode("utf-8")
                df = subStr[1]
                self.dfMap[word] = int(df)

            def txtInfoSaturation(self, txt):
                sum = 0.0
                uni_str = unicode(self.SplitterCh_Utf8(txt))
                slen = len(uni_str)
                for i in range(slen):
                    try:
                        df = self.dfMap[uni_str[i]]
                        x = df * 1.0 / (self.totalDf * 2.0)
                        ent = 1.0 + (x * math.log(x, 2.0) + (1.0 - x) * math.log((1.0 - x), 2.0))
                        sum += ent
                    except Exception as e:
                        continue
                return sum / 140.0

if __name__ == "__main__":
    ch = ChInfoEnt()
    #ch.LoadChDfStat("./data/ch_df_stat")
    # txt = "欧弟节目恶搞王宝强离婚 扮演宋喆版杨康】近日，欧弟在一个《离婚风波》小品中疑影射#王宝强离婚#风波。小品讲述郭靖黄蓉因离婚闹公堂，一代大侠被兄弟戴上绿帽子的故事。将王宝>强和马蓉事件翻版搬上荧幕，有网友表示小品很搞笑，也有人觉得这样揭人伤疤，很没品…你怎么看？"
    # txt = "【王楠老公删光王宝强相关微博】近日，王楠老公郭斌将微博中有关#王宝强#的内容全部删除，甚至有网友透露，如果在其微博下评论王宝强的相关内容，也会被拉黑。据悉，@亲见郭斌 与@王宝强私交甚笃，不仅在  # 王宝强离婚#事件中力挺他，而且在10月22日在微博晒出了两人一起打高尔夫的照片"
    # txt = "#长春国贸# 自8月14日王宝强发布离婚声明，至今两个多的时间，马蓉掉了近百万粉丝，她取关了29个人，包括几位圈内明星！"
    # txt = "#衣品天成全明星#爱笑、爱美、爱生活！快跟我一起去衣品天成打造完美自己！"
    # txt = "【每日一推】推荐一下谷歌DeepMind在NIPS上发的关于利用Recurrent Attention Networks做的图像识别的文章《Recurrent Models of Visual Attention》"
    # txt = "3140再次强势突破！！历史总是惊人相似，又被我说中了，煤炭有色再次证明了我的理论。最近天天熬夜复盘到2点，下个热点板块龙头股隐隐有抬头迹象，没关注我的看来是又要错过了。>没关注我的，右上角关注，私信找我助手拿"
    txt = "次强势突破!you are the one,I'm"
    # txt = ch.SplitterCh_Utf8(txt)
    txt = ch.SpliterEn_Utf8(txt)
    print txt
    # print ch.txtInfoSaturation(txt)
    # print ch.dfMap
