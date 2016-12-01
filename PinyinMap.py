#-*-coding:utf-8-*-
import sys
import codecs

class PinyinMap(object):
    def __init__(self):
        self.m_mapBiChar2PinyinCode={}
        self.m_maxPinyinCode = 1

    def ReadPinyinMap(self,sFile):
        mapPy2Code = {}
        for line in codecs.open(sFile,'r',"utf-8"):
            if not line:
                continue
            pyArray=line.strip("\n").split("|")
            pyCode = mapPy2Code.get(pyArray[1])
            if not pyCode:
                self.m_maxPinyinCode +=  1
                pyCode = self.m_maxPinyinCode
                mapPy2Code[pyArray[1]] = pyCode
            item = []
            item.append(pyArray[1])
            item.append(pyCode)
            self.m_mapBiChar2PinyinCode[pyArray[0]] = item
    def GetCode(self,sCh):
        pyMap = self.m_mapBiChar2PinyinCode.get(sCh)
        if pyMap:
            return pyMap[1]
        else:
            return 0

    def GetPinyin(self,sCh):
        pyMap=self.m_mapBiChar2PinyinCode.get(sCh)
        if pyMap:
            return pyMap[0]
        else:
            return None

    def GetSize(self):
        return self.m_maxPinyinCode

class CnStrPinyinEncoder(object):
    def __init__(self):
        self.PinyinMap = PinyinMap()

    #载入拼音映射表
    def LoadPinyinMap(self,sFile):
        return self.PinyinMap.ReadPinyinMap(sFile)

    #拼音编码串的长度
    def PinyinCode(self,sStr):
        unLen = len(sStr)
        encode = [0]*unLen
        pos = 0
        unOffset = 0
        code = -1
        while pos < unLen:
            if sStr[pos]:
                code=self.PinyinMap.GetCode(sStr[pos])
                if (code >> 8) > 0 :
                    encode[unOffset] = code % 255
                else:
                    encode[unOffset] = code
                unOffset += 1
                pos += 1

        return (unOffset,encode)

    def SplitterCh_Utf8(self,str_txt):
        uni_str = unicode(str_txt, "utf-8")
        slen = len(uni_str)

        uni_ch_str = ""
        for i in range(slen):
            uchar = uni_str[i]
            if uchar >= u'\u4e00' and uchar<= u'\u9fa5':
                uni_ch_str += uchar
            else:
                pass
        #utf8_str = uni_ch_str.encode("utf-8")
        #return utf8_str
        spliter_str = uni_ch_str[0:30]
        return spliter_str

    #对字符串进行拼音编码，每n个汉字拼音构成一个特征码（n=8,4,2)
    def Encode_8CnChar(self,sStr):
        setPinyinCode = set()
        setPinyinCode.clear()
        sStr = self.SplitterCh_Utf8(sStr)
        size,encoded = self.PinyinCode(sStr)
        if size >=8:
            for i in range(size - 8):
                coder = encoded[i] << 8*7
                for j in range(1,8):
                    coder |= encoded[i] << 8*(7 - j)
                setPinyinCode.add(coder)
        return setPinyinCode

    def Encode_4CnChar(self,sStr):
        setPinyinCode = set()
        setPinyinCode.clear()
        sStr = self.SplitterCh_Utf8(sStr)
        size,encoded = self.PinyinCode(sStr)
        if size >=4:
            for i in range(size - 4):
                coder = encoded[i] << 8*3
                for j in range(1,4):
                    coder |= encoded[i] << 8*(3 - j)
                setPinyinCode.add(coder)
        return setPinyinCode

    def Encode_2CnChar(self,sStr):
        setPinyinCode = set()
        setPinyinCode.clear()
        sStr = self.SplitterCh_Utf8(sStr)
        size,encoded = self.PinyinCode(sStr)
        if size >= 2:
            print range(size - 2)
            for i in range(size - 2):
                coder = encoded[i] << 8*1
                for j in range(1,2):
                    coder |= encoded[i] << 8*(1 - j)
                setPinyinCode.add(coder)
        return setPinyinCode

if __name__=="__main__":
    pm = PinyinMap()
    #pm.ReadPinyinMap("../data/cnchar_to_pinyin.map")
    #print pm.GetSize()
    #print pm.GetPinyin(unicode("中","utf-8"))

    pc = CnStrPinyinEncoder()
    pc.LoadPinyinMap("../data/cnchar_to_pinyin.map")
    sStr1 = "#扇贝打卡# 扇贝英语阅读和单词特训第123天：完成2篇文章，52个单词，明天继续http://t.cn/Rf9BsiK"
    sStr2 = "#扇贝打卡# 和单词特训第202天：完成3篇文章，164个单词，明天继续http://t.cn/Rf9B3Vb"

    encode1 = pc.Encode_4CnChar(sStr1)
    encode2 =  pc.Encode_4CnChar(sStr2)

    same = len(set(encode1).intersection(set(encode2)))
    sim = float(same)/(len(encode1) + len(encode2) - same)
    print sim