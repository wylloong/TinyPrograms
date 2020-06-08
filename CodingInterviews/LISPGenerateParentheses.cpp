/*******************************************************************
Copyright(c) 2017, waylon
All rights reserved.
Distributed under the BSD license.
Blog: http://www.cnblogs.com/DHUtoBUAA/
*******************************************************************/
/*
题目描述：
LISP语言唯一的语法就是括号要匹配。
形如（OP P1 P2 …），括号内元素由单个空格分割。
其中第一个元素OP为操作符，后续元素均为其参数，参数个数取决于操作符类型
注意：参数P1,P2也有可能是另外一个嵌套的（OP P1 P2 …）
其中OP类型为add/sub/mul/div（全小写），分别代表整数的加减乘除法
其中add/mul参数个数2或以上，sub/div参数个数为2
举例：
-输入：（mul 3 -7） 输出：-21
-输入：（add1 2 3） 输出：6
-输入：（sub (mul 2 4) (div 9 3)） 输出：5
-输入：（div 1 0） 输出：error

题目涉及数字均为整数，可能为负；不考虑32位溢出翻转
除零错误时，输出"error"，除法遇除不尽，取整，即3/2=1

输入描述：
合法C字符串，字符串长度不超过512；用例保证了无语法错误

输出描述：
合法C字符串，字符包括'0'-'9'及负号'-'或者'error'

示例
输入 （add 1 2 3） 输出 6
*/

#include <iostream>
#include <algorithm>
#include <string>
#include <stack>
#include <vector>
#include <cstdio>
#include <stdlib.h>
#include <cstring>

using namespace std;

int main()
{
	char chs[512];
	bool error = false;
	gets_s(chs);  
	//gets(chs); //old version
	std::string str(chs);
	std::stack<std::string> opstack;	// operations
	std::stack<std::string> strstack;	// divided strings
	for (int i = 0; i < str.size();)
	{
		if (str[i] == ' ')
		{
			i = i + 1;
			continue;
		}
		if (str[i] == '(')
		{
			strstack.push(std::string("("));
			int spaceIndex = str.find(' ', i);
			std::string tmp = str.substr(i + 1, spaceIndex - i - 1);
			opstack.push(tmp);  // operation
			i = spaceIndex;
		}
		else if (str[i] == ')')
		{
			std::string curOp = opstack.top();
			opstack.pop();
			std::vector<std::string> tmps; // strs temp
			while (strstack.top() != "(")
			{
				tmps.push_back(strstack.top());
				strstack.pop();
			}
			strstack.pop();
			// add
			if (curOp == "add")
			{
				int temp = 0;
				for (int i = 0; i<=tmps.size() - 1; ++i)
				{
					temp += atoi(tmps[i].c_str());
				}
				strstack.push(to_string(temp));
			}
			// sub
			else if (curOp == "sub")
			{
				int temp = 0;
				if (tmps.size() > 0)
					temp = atoi(tmps[tmps.size() - 1].c_str());
				for (int i = tmps.size() - 2; i >= 0; --i)
				{
					temp -= atoi(tmps[i].c_str());
				}
				strstack.push(to_string(temp));
			}
			// mul
			else if (curOp == "mul")
			{
				int temp = 0;
				if (tmps.size() > 0)
					temp = atoi(tmps[tmps.size() - 1].c_str());
				for (int i = tmps.size() - 2; i >= 0; --i)
				{
					temp *= atoi(tmps[i].c_str());
				}
				strstack.push(to_string(temp));
			}
			// div
			else if (curOp == "div")
			{
				int temp = 0;
				if (tmps.size() > 0)
					temp = atoi(tmps[tmps.size() - 1].c_str());
				for (int i = tmps.size() - 2; i >= 0; --i)
				{
					int data1 = atoi(tmps[i].c_str());
					if (data1 == 0)
					{
						error = true;
						break;
					}
					else
						temp /= data1;
				}
				if (error)
					break;
				else
					strstack.push(to_string(temp));
			}
			++i;
		}
		else  // substrs
		{
			// get substring by ' ' or ')'
			auto index = str.find(' ', i);
			auto index2= str.find(')', i);
			if (index < index2)
			{
				strstack.push(str.substr(i, index - i));
				i = index;
			}
			else
			{
				strstack.push(str.substr(i, index2 - i));
				i = index2;
			}
		}
	}
	if (error)
		cout << "error";
	else
		cout << atoi(strstack.top().c_str());
	return 0;
}
