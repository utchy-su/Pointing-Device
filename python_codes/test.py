sampleList = [1, 2, 3]

def sumList(li):
	answer = 0
	for value in li:
		answer = answer + value
		print(answer)

	return answer

ans = sumList(sampleList)
print("final answer is", ans)
