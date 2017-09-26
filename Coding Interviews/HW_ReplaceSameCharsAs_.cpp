/*
题目描述
输入两个字母串，将两个字母串都包含的字母用'_'替换后，输出两个字母串的剩余部分。
输入描述:
输入两个字符串，字符串最大长度为100。字符串只包含字母，不可能为空串，区分大小写。
输出描述:
按字符串顺序输出处理后的字符串
示例1
输入
abcd
bdef
输出
a_c_ 
__ef

思路：对输入的两个字符串分别建立hash表，字符串中的每一个字符根据两个hash表判断是否是两个子母串都包含的字母，如果是用'_'替换，否则输出原字符。
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
	string firstStr;
	string secondStr;
	cin >> firstStr;
	cin >> secondStr;

	const int tableSize = 256;
	// 第一个hash表
	unsigned int hashTable1[tableSize];
	for (unsigned int i = 0; i<tableSize; i++)
		hashTable1[i] = 0;
	const char* pHashKey1 = firstStr.c_str();
	while (*(pHashKey1) != '\0')
		hashTable1[*(pHashKey1++)]++;
	// 第二个hash表
	unsigned int hashTable2[tableSize];
	for (unsigned int i = 0; i<tableSize; i++)
		hashTable2[i] = 0;
	const char* pHashKey2 = secondStr.c_str();
	while (*(pHashKey2) != '\0')
		hashTable2[*(pHashKey2++)]++;

	//输出
	pHashKey1 = firstStr.c_str();
	while (*(pHashKey1) != '\0')
	{
		if (hashTable1[*(pHashKey1)] > 0 && hashTable2[*(pHashKey1)] > 0)
		{
			//具有重复字符
			cout << "_";
		}
		else
			cout << *(pHashKey1);
		pHashKey1++;
	}
	cout << endl;
	pHashKey2 = secondStr.c_str();
	while (*(pHashKey2) != '\0')
	{
		if (hashTable1[*(pHashKey2)] > 0 && hashTable2[*(pHashKey2)] > 0)
		{
			//具有重复字符
			cout << "_";
		}
		else
			cout << *(pHashKey2);
		pHashKey2++;
	}
	return 0;
}
