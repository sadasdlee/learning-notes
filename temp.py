"""
给定一个字符串 s ，请你找出其中不含有重复字符的 最长 子串 的长度。

 

示例 1:

输入: s = "abcabcbb"
输出: 3 
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。注意 "bca" 和 "cab" 也是正确答案。
示例 2:

输入: s = "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
示例 3:

输入: s = "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
     请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。
"""

            
class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        stack = [0] * len(s)
        stack_index = -1

        for i in range(len(s)):
            ch = s[i]
            if ch == '(' or ch == '[' or ch == '{':
                stack[stack_index + 1] = ch
                stack_index += 1
                continue
            if stack_index < 0:
                return False
            else:
                if ch == ')' and stack[stack_index] == '(':
                    stack_index -= 1
                elif ch == ']' and stack[stack_index] == '[':
                    stack_index -= 1
                elif ch == '}' and stack[stack_index] == '{':
                    stack_index -= 1
                else:
                    return False
        if stack_index == -1:
            return True
        return False