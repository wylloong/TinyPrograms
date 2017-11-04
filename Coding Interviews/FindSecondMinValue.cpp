/*******************************************************************
Copyright(c) 2017, waylon
All rights reserved.
Distributed under the BSD license.
*******************************************************************/

#include<iostream>
#include<stdlib.h>
using namespace std;
typedef struct BSTreeNode {
	int m_nValue;
	struct BSTreeNode * m_pLeft;
	struct BSTreeNode * m_pRight;
	BSTreeNode(int x) :m_nValue(x), m_pLeft(NULL), m_pRight(NULL) {}
}BSTreeNode;

BSTreeNode * creatBTree(int data[], int index, int n) {
	BSTreeNode * pNode = NULL;
	cout << "creat node " << index << endl;
	if (index < n && data[index] != -1) //数组中-1 表示该节点为空
	{
		cout << " with data " << data[index] << endl;
		pNode = new BSTreeNode(data[index]);
		if (pNode == NULL)
			return NULL;
		pNode->m_pLeft = creatBTree(data, 2 * index + 1, n); //将二叉树按照层序遍历, 依次标序号, 从0开始
		pNode->m_pRight = creatBTree(data, 2 * index + 2, n);
	}
	else {
		cout << " with NULL " << endl;
	}
	return pNode;
}
void deleteTree(BSTreeNode *node) {
	if (node->m_pLeft) {
		deleteTree(node->m_pLeft);
	}
	if (node->m_pRight) {
		deleteTree(node->m_pRight);
	}
	free(node);
	return;
}

void printTree(BSTreeNode *node) {
	if (node != NULL) {
		cout << node->m_nValue << " ";
		printTree(node->m_pLeft);
		printTree(node->m_pRight);
	}
	return;
}

class Solution {
public:
	int findSecondMinimumValue(struct BSTreeNode *root) {
		/*
		*在编写输入你的代码
		*/
		if (root == nullptr)
			return -1;
		int firstMin = root->m_nValue;   //第一小初始化
		int secondMin = 0x7FFFFFFF;  //第二小初始化
		findSecondMinimumValueCore(root, firstMin, secondMin);
		if (secondMin == 0x7FFFFFFF)  //如果没有第二小的值，secondMin未赋值，给出-1
			return -1;
		return secondMin;
	}

	void findSecondMinimumValueCore(struct BSTreeNode *root,int firstMin,int& secondMin)
	{
		// 前序遍历
		int value = root->m_nValue;
		if (firstMin<value && secondMin>value)
			secondMin = value;
		if (root->m_pLeft && root->m_pLeft->m_nValue<secondMin) 
			// 剪枝，因为每一个节点的值小于等于它的子节点的值，如果该节点大于等于secondMin的值，则无需遍历，需要做剪枝提高效率
			findSecondMinimumValueCore(root->m_pLeft, firstMin, secondMin);
		if(root->m_pRight && root->m_pRight->m_nValue<secondMin)
			findSecondMinimumValueCore(root->m_pRight, firstMin, secondMin);
	}
};

int test_solution(int data[], int length) 
{
	BSTreeNode* root = creatBTree(data, 0, length);
	printTree(root);
	cout << endl;
	Solution solution;
	int val = solution.findSecondMinimumValue(root);
	cout << "finall the res = " << val << endl;
	deleteTree(root);
	return val;
}

int main() {
	int a[] = { 2,2,5,-1,-1,5,7 };
	int b[] = { 2,2,2 };
	int c[] = { 1,1,3,1,1,3,4,3,1,1,1,3,8,4,8,3,3,1,6,2,1 };
	test_solution(a, sizeof(a) / sizeof(int));
	test_solution(b, sizeof(b) / sizeof(int));
	test_solution(c, sizeof(c) / sizeof(int));
	return 0;
}
