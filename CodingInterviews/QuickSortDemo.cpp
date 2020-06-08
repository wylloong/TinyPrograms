/*******************************************************************
Copyright(c) 2017, waylon
All rights reserved.
Function: 快排递归和非递归实现源代码
Distributed under the BSD license.
*******************************************************************/

#include<cstdio>
#include<exception>
#include<algorithm> 
#include<stack>

using namespace std;

int RandomInRange(int start, int end)
{
	if (end > start)
	{
	  srand(time(NULL));
	  return start + rand() % (end - start);
	}
}

void Swap(int& elem1, int& elem2)
{
	int temp;
	temp = elem1;
	elem1 = elem2;
	elem2 = temp;
}

// Partition函数除了可以用在快速排序算法中，还可以用来实现在长度为n的数组中查找第k大的数字。
int Partition(int data[], int length, int start, int end)
{
	if (data == nullptr || length <= 0 || start<0 || end >= length)
		throw new std::exception("Invalid Parameters!");
	//return 0;

	int index = RandomInRange(start, end);  // 生成一个在start和end之间的随机数
	Swap(data[index], data[end]);   // 函数Swap的作用是用来交换两个数字

	int small = start - 1;
	for (int index = start; index<end; ++index)
	{
		if (data[index]<data[end])
		{
			++small;
			// 小的数移动到右边
			if (small != index)
				Swap(data[index], data[small]);
		}
	}
	++small;
	Swap(data[small], data[end]);  // 中间数归位
	return small;
}

// 使用递归的思想分别对每次选中的数字的左右两边排序
void QuickSort(int data[], int length, int start, int end)
{
	if (end == start)
		return;
	int index = Partition(data, length, start, end);
	if (index>start)
		QuickSort(data, length, start, index - 1);
	if (index<end)
		QuickSort(data, length, index + 1, end);
}


void quickSortNonRecursive(int data[], int length, int start, int end)
{
	std::stack<int> s;
	if (start<end)
	{
		int mid = Partition(data, end- start+1,start, end);
		if (mid - 1>start)
		{
			// 左边不止一个元素
			s.push(start);
			s.push(mid - 1);
		}
		if (mid + 1<end)
		{
			s.push(mid + 1);
			s.push(end);
		}
		while (!s.empty())
		{
			int qHeight = s.top();
			s.pop();
			int pLow = s.top();
			s.pop();
			int pqMid = Partition(data, qHeight- pLow+1, pLow, qHeight);
			if (pqMid - 1 > pLow)
			{
				s.push(pLow);
				s.push(pqMid - 1);
			}
			if (pqMid + 1 < qHeight)
			{
				s.push(pqMid + 1);
				s.push(qHeight);
			}
		}

	}
}

int main()
{
	int data[8] = { 0,2,4,6,1,3,5,7 };
	// 对一个长度为n的数组排序，只需要把start设置为0,把end设置为n-1,调用函数QuickSort即可。
	//QuickSort(data, 8, 0, 7);  //递归方法
	quickSortNonRecursive(data, 8, 0, 7);  //非递归方法
	for (int i = 0; i<8; i++)
		printf("%d \t", data[i]);
	getchar();
	return 0;
}
