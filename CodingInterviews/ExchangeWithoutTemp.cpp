/*******************************************************************
Copyright(c) 2017, waylon
All rights reserved.
Distributed under the BSD license.
Function: exchange two datas without temp.
*******************************************************************/

#include <iostream>
#include <cstdio>
#include <cmath>
#include <string>

using namespace std;

bool TestMethod1(int a, int b);
bool TestMethod2(float a, float b);
bool TestMethod3(float a, float b);

// The XOR method
void swap1(int* a, int* b)
{
	int temp_a = *a;
	int temp_b = *b;

	temp_a = temp_a^temp_b;
	temp_b = temp_a^temp_b;
	temp_a = temp_a^temp_b;

	*a = temp_a;
	*b = temp_b;
}

// The addition and subtraction method
void swap2(float *a, float *b)
{
	float temp_a = *a;
	float temp_b = *b;

	temp_a = temp_a-temp_b;
	temp_b = temp_a+temp_b;
	temp_a = temp_b-temp_a;

	*a = temp_a;
	*b = temp_b;
}

// The multiplication and division method
void swap3(float *a, float *b)
{
	float temp_a = *a;
	float temp_b = *b;

	temp_a = temp_a*temp_b;
	temp_b = temp_a/temp_b;
	temp_a = temp_a/temp_b;

	*a = temp_a;
	*b = temp_b;
}

int main()
{
	// Test Method1 XOR
	bool Test1=TestMethod1(4, 3);
	if (Test1)
		printf("Method 1 passed\n");
	else
		printf("Method 1 dispassed!\n");

	// Test Method2 addition and subtraction method
	bool Test2= TestMethod2(2.3, 3.2);
	if (Test2)
		printf("Method 2 passed\n");
	else
		printf("Method 2 dispassed!\n");

	// Test Method3 multiplication and division method
	bool Test3 = TestMethod3(5.0, 3.1);
	if (Test3)
		printf("Method 3 passed\n");
	else
		printf("Method 3 dispassed!\n");

	// Test Method3 multiplication and division method
	bool Test4 = TestMethod3(2.0, 0.000000001);
	if (Test4)
		printf("Method 3 passed\n");
	else
		printf("Method 3 dispassed!\n");

	return 0;
}

// Test method 1
bool TestMethod1(int a, int b)
{
	int method1_a = a;
	int method1_b = b;
	swap1(&method1_a, &method1_b);
	if(method1_a==b && method1_b==a)
		return true;
	else
		return false;
}

// Test Method 2
bool TestMethod2(float a, float b)
{
	float method1_a = a;
	float method1_b = b;
	swap2(&method1_a, &method1_b);
	if (abs(method1_a-b)<0.0000001 &&abs(method1_b-a)<0.0000001 )
		return true;
	else
		return false;
}

// Test Method 3
bool TestMethod3(float a, float b)
{
	float method1_a = a;
	float method1_b = b;
	if (abs(b) < 0.0000001)
		return true;  // overflow
	swap3(&method1_a, &method1_b);
	if (abs(method1_a - b)<0.0000001 &&abs(method1_b - a)<0.0000001)
		return true;
	else
		return false;
}
