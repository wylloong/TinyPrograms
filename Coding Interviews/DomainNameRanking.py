'''
题目描述
主机名由多级域名组成，自右向左，依次是顶级域名、二级域名、三级域名…..以此类推
例，主机名：google.com.hk
hk是顶级域名
com是二级域名
google是三级域名
现在我们需要实现一个主机名的排序功能
排序规则
1）主机名按照域名等级排序，即先按照顶级域名排序，顶级域名相同的再按照二级域名排序，顶级和二级域名均相同的再按照三级域名排序，以此类推，直到整个主机名排序完毕
2）如果短主机名是由长主机名从顶级域名开始的连续一个或多个域名组成，短主机名排在长主机名前面。例：google.com 排在 gmail.google.com 之前
3）每一级域名按照字典顺序排序，字典顺序定义见下页
输入确保符合以下规则（无需检查）
1）主机名以字符串形式给出，非空串
2）主机名中仅包含小写英文字母和分隔符’.’
3）主机名中没有连续的’.’，不以’.’开始，也不以’.’结束
3）主机名不存在重复
1、两个单词(字母按照自左向右顺序)先以第一个字母作为排序的基准，如果第一个字母相同，就用第二个字母为基准，如果第二个字母相同就以第三个字母为基准。依此类推，如果到某个字母不相同，字母顺序在前的那个单词顺序在前。
例：abc 排在 abf 之前
2、如果短单词是长单词从首字母开始连续的一部分，短单词顺序在前。
例：abc 排在 abcd 之前
输入描述:
不超过255个字符的字符串，不同的域名间用字符'|'进行分隔。
输出描述:
排序后的的域名，域名间用字符'|'进行分隔。
示例1
输入
mail.huawei.com|huawei.com|teltalk.org|google.com.hk|imail.huawei.com
输出
huawei.com|imail.huawei.com|mail.huawei.com|google.com.hk|teltalk.org

思路：首先根据“|”字符来分割输入字符串，保存到list中。结合插入排序的思想，依次将一个域名插入排序好的域名序列中，完成域名的排序！
'''

# coding=utf-8
strInput=raw_input()
#strInput="mail.huawei.com|huawei.com|imail.huawei.com|teltalk.org|google.com.hk|google.com.hk";
strDomainList=strInput.split('|')
sortedDomainList=[]
# compared
while len(strDomainList)>0:
    index=0
    add=False
    while index<len(sortedDomainList):
        comp2=sortedDomainList[index].split('.')
        compareStr=strDomainList[0].split('.')
        while(len(compareStr)>0 and len(comp2)>0):
            if cmp(compareStr[len(compareStr)-1],comp2[len(comp2)-1])<0:
                # 小于,插在前面
                add=True
                sortedDomainList.insert(index,strDomainList[0])
                del strDomainList[0]
                break
            elif cmp(compareStr[len(compareStr)-1],comp2[len(comp2)-1])==0:
                # 等于
                del compareStr[len(compareStr)-1]
                del comp2[len(comp2)-1]
            else:
                # 大于，下一个
                break
        if add==False:
            if len(compareStr)==0:
                add = True
                sortedDomainList.insert(index, strDomainList[0])
                del strDomainList[0]
        index+=1
        if add==True:
            break
    if add==False:
        sortedDomainList.append(strDomainList[0])
        del strDomainList[0]
output=""
index=1
output+=sortedDomainList[0]
while index<len(sortedDomainList):
    temp="|"+sortedDomainList[index]
    output += temp
    index+=1
print output
