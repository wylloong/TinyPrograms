/*******************************************************************
Copyright(c) 2017, waylon
All rights reserved.
Distributed under the BSD license.
*******************************************************************/

#include<cstdio>
#include<iostream>
#include<string>
#include<vector>
#include<cstdio>
#include<fstream>
#include<time.h>
using namespace std;

void FindNumsAppearOnce(vector<int> data, int length, int *num1)
{
	if (length<2)
		return;

	int resultExclusiveOR = 0;
	for (int i = 0; i<length; i++)
		resultExclusiveOR ^= data[i];
	*num1 = resultExclusiveOR;
}

// ==================== Test Code ====================
void Test(const char* testName, vector<int> data, int length, int expected1)
{
	if (testName != nullptr)
		printf("%s begins: ", testName);

	int result1, result2;
	FindNumsAppearOnce(data, length, &result1);
	if ((expected1 == result1))
		printf("Passed.\n");
	else
		printf("Failed.\n");
}

void XORCore(string filepath,string testname,int expected1)
{
	// timer
	clock_t start1 = clock();
	vector<int> inputStr;
	string temp;
	// read files
	std::ifstream myfile(filepath);
	if (!myfile.is_open())
	{
		cout << "Open faile!" << endl;
	}
	while (getline(myfile, temp))
	{
		inputStr.push_back(atoi(temp.c_str()));
	}
	Test(testname.c_str(), inputStr, inputStr.size(), expected1);
	clock_t ends1 = clock();
	cout << "Running Time : " << (double)(ends1 - start1) / CLOCKS_PER_SEC << "s" << endl<<endl;
}

int main(int argc, char* argv[])
{
	//输入参数：文件路径、测试名称、期望结果
	XORCore("E:\\array_1.txt", "Test1",1927);
	XORCore("E:\\array_2.txt", "Test2", 16722);

	return 0;
}
