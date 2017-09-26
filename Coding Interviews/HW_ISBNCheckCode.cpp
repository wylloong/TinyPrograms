/*
题目描述
一本正式出版的图书都有一个ISBN号码与之对应，ISBN码包括9位数字、1位识别码和3位分隔符，其规定格式如“x-xxx-xxxxx-x”，其中符号“-”是分隔符（键盘上的减号），最后一位是识别码，例如0-670-82162-4就是一个标准的ISBN码。ISBN码的首位数字表示书籍的出版语言，例如0代表英语；第一个分隔符“-”之后的三位数字代表出版社，例如670代表维京出版社；第二个分隔之后的五位数字代表该书在出版社的编号；最后一位为识别码。识别码的计算方法如下：
首位数字乘以1加上次位数字乘以2……以此类推，用所得的结果mod 11，所得的余数即为识别码，如果余数为10，则识别码为大写字母X。例如ISBN号码0-670-82162-4中的识别码4是这样得到的：对067082162这9个数字，从左至右，分别乘以1，2，…，9，再求和，即0×1+6×2+……+2×9=158，然后取158 mod 11的结果4作为识别码。
你的任务是编写程序根据输入的ISBN号码的前3段，计算出识别码，并输出完整的ISBN码。
输入描述:
为一个ASCII字符串。内容为ISBN码的前三段，以上面为例，就是0-670-82162。
输出描述:
若判断输入为合法的字符串，则计算出识别码，并输出完整的ISBN码；
若输入不合法，则输出字符串”ERROR”；

注意：最终交付的函数代码中不要向控制台打印输出任何无关信息。
示例1
输入
0-670-82162

输出
0-670-82162-4

思路：先判断输入的字符串是否合法，合法后分解字符串为字符保存到数组中，然后根据公式依次计算字符的乘积，最后取余，但是需要注意10的输出具有特殊性！
*/

#include <iostream>
#include <cstdio>
#include <stdlib.h>
#include <cmath>
#include <string>
#include <vector>
#include <stack>
#include <queue>
#include <algorithm>
#include <set>
using namespace std;

int main()
{
	string inputStr="";
	std::cin >> inputStr;
	//inputStr = "0-670--2162";
	//cout << inputStr;
	string outputStr = "ERROR";
	if (inputStr.size() == 11)
	{
		//长度符合
		vector<int> diviData;
		for (int i = 0; i < inputStr.size(); i++)
		{
			if (i == 1 || i == 5)
			{
				if (inputStr[i] == '-')
				{

				}
				else
				{
					//格式不正确
					break;
				}
			}
			else
			{
				char tempChar = inputStr[i];
				if (tempChar <= '9' && tempChar >= '0')
				{
					diviData.push_back(tempChar-'0');
				}
				else
				{
					//格式不正确
					break;
				}
			}
			if (i == (inputStr.size() - 1))
			{
				int sum = 0;
				//计算输出
				for (int i = 0; i < 9; i++)
				{
					sum += diviData[i] * (i +1 );
				}
				int outChar = sum % 11;
				string subStr = "";
				if (outChar == 10)
				{
					subStr = "-X";
					outputStr = inputStr + subStr;
				}
				else
				{
					//outChar.
					switch (outChar)
					{
					    case 0:
							subStr = "0";
							break;
						case 1:
							subStr = "1";
							break;
						case 2:
							subStr = "2";
							break;
						case 3:
							subStr = "4";
							break;
						case 4:
							subStr = "4";
							break;
						case 5:
							subStr = "5";
							break;
						case 6:
							subStr = "6";
							break;
						case 7:
							subStr = "7";
							break;
						case 8:
							subStr = "8";
							break;
						case 9:
							subStr = "9";
							break;
					}
					outputStr = inputStr + "-" + subStr;
				}
			}
		}
	}
	// 输出
	cout << outputStr;
	return 0;
}
