# def lengthOfLongestSubstring(s):
#     """
#     :type s: str
#     :rtype: int
#     """
#     s_list =

a = 'abcabcbb'

a_list = list(a)
lop = 0
for i in range(0, len(a_list)):
    temp = [a_list[i]]
    for j in range(1, len(a_list)-i):
        if a_list[i+j] not in temp:
            temp.append(a_list[i+j])
        else:
            break
    if len(temp) > lop:
        lop = len(temp)
print(lop)