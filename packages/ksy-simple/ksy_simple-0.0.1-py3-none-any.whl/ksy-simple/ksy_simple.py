import numpy

def max_power_of_q_below_n(n,q): #n:n이하로 가장 큰 q의 몇승의 숫자
    m=0
    while n>=q**m:
        if n<q**(m+1):
            print(m+1,"일때 ",q**(m+1))
            return m, q**m
        m+=1
    #처음에 뒤집어 주는거 하기 싫어서 먼저 어디부터 내림차순해야 편할까
    #구해서 할까했는데 오히려 그냥 오름으로 구하고 뒤집는게 연산량상 적겠다 판단

#q진법 변환기
def convert_to_base(n,q): #n숫자, q진법
    rev_b=[]
    if n>q**30:
        print("숫자 너무커서 예상범위 벗어남")
    for i in range(1,30):
        if (q**i) < n:
            a=(n//(3**(i-1))) #몫
            b=a%3#나머지
            rev_b.append(b)
            if a<9 :
                rev_b.append(a//3)
    print(rev_b) #작은것부터 들어가서 뒤집어줘야함

    return rev_b[::-1]

#더 짧고 빠를 것으로 예상 (최적화랄까)
def con_n(n,q): #n진법 변환기 (conversion to base n)
    rev_base = ''

    while n > 0:
        n, mod = divmod(n, q)
        rev_base += str(mod)

    return rev_base[::-1]            

#약수들의 합
def sum_of_divisors(num):
    return num + sum([i for i in range(1, (num // 2) + 1) if num % i == 0])

#약수의 갯수
def divisor_count(num): #확인범위 제곱근으로 줄여서 더빠름
    count=0
    for i in range(1,int(num ** 0.5)+1): #제곱근한 값의 이전까지 체크
        if num/i==i:
            count+=1
        elif num % i ==0:
            count+=2
    return count

#약수의 갯수
def divisor_count2(num): #확인범위 1/2으로 하여 조금 느림 (전부보는 것보단 빠름)
    count=1
    for i in range(1,(num // 2) + 1):
        if num % i ==0:
            count+=1
    return count

#약수들의 리스트
def divisors_list(num):
    return [i for i in range(1, (num // 2) + 1) if num % i == 0]+[num]

#n/2과 n**0.5 비교해보면 0<n<4의 경우만 n/2이 더 작고 ->1,2,3뿐이고 갯수 적음
#나머진 n**0.5의 경우가 더 작음
#그런데 단순 약수 구할 때는 n/2까진 해줘야 알맞게 계산되네

#소수 판별함수
def prime_num(num):
    for i in range(2, int(num**0.5)+1): # n의 제곱근을 정수화 시켜준 후 + 1
        if num % i == 0:
            return False
    return True

#소수 구하는 리스트 (num이하)
def prime_num_list(num):
    a=[]
    for i in range(2,num+1):
        check=1 #나눠지는 수가 확인되면 패스하는 스위치 1일때는 수행함
        for j in range(2, int(i**0.5)+1): # n의 제곱근을 정수화 시켜준 후 + 1
            if i % j == 0:
                check=0 #0되면 해당 숫자 패스
                break
        if check == 0:
            continue
        a.append(i)
    return a

#소인수분해 함수 우선 소인수 종류목록만 먼저 짜고, 소인수분해형태로
def prime_factors_list(n):
    a=[]
    for i in range(2, (n // 2) + 1):
        if n % i == 0:
            check=1
            for j in a:
                if i % j == 0:
                    check=0 #0되면 해당 숫자 패스
                    break
            if check == 0:
                continue
            a.append(i)
    if len(a)==0: #소수가 입력된 경우 추가
        a.append(n)
    print("소인수 목록",a)
    n_def=n #원래 n값 기억
    c_m=[]
    for k in range(len(a)):
        n=n_def
        count=0 #몇 번 나눠지는지 체크
        while n%a[k] == 0 :
            n=n//a[k]
            count+=1
        c_m.append(count)
        #자동으로 만약 200이라 a=[2,5],c_m=[3,2]이면
        #[2,2,2,5,5]이런식으로 나오게 하고 싶었는데 일일히 반복문써서
        #하는거말곤 깔끔히 하는 테크닉이 안떠올라서 일단 여기서 스톱
    return a,c_m

#최대공약수와 최소공배수
def gcdlcm(n, m):
    x=ftn3(n)
    y=ftn3(m)
    print(x)
    print(y)
    gcd=1
    for z in range(len(x[0])):
        if x[0][z] in y[0]:
            print(y[1][(y[0].index(x[0][z]))])
            gcd*=x[0][z]**(min(x[1][z],y[1][(y[0].index(x[0][z]))]))
            
    return [gcd,n*m//gcd]

def gcdlcm_euclid(a, b): #유클리드 호제법으로 잘짜둔것 가져온것 (속도 압도적이다..)
    c,d = max(a, b), min(a, b)
    t = 1
    while t>0:
        t = c%d
        c, d = d, t
    answer = [ c, int (a*b/c)]
    return answer


#메모이제이션 방식 채택 (아래 가져온 코드들과 다른 곳에서 참조)
#https://richwind.co.kr/3
def fib(n):
    fibList=[1, 1]
    if n==1 or n==2:
        return 1
    for i in range(2,n):
        fibList.append( fibList[i-1] + fibList[i-2] )
        num=fibList[-1]
    return num

#https://pacific-ruler.tistory.com/entry/Python-%ED%94%BC%EB%B3%B4%EB%82%98%EC%B9%98-%EC%88%98%EC%97%B4-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0-%EC%97%AC%EB%9F%AC%EA%B0%80%EC%A7%80-%EB%B0%A9%EB%B2%95-%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8-%EC%A4%91
#재귀함수 방식 내가 옛날에 배울 때 해봤던 방식
#그런데 가장 느리다고 한다
def fibo_recur_1(n): 
    result = []
    if n <= 2:
        number = 1
    else:
       number = fibo_recur(n-1) + fibo_recur(n-2)
    return number

#while 반복문
def fibo_while (n) :
    result = []
    a, b = 1, 1
    while a < n:
        a, b = b, a + b
        result.append(a)  
    return a

#for 반복문
def fibo_for(n):
    result = []
    a, b = 1, 1
    for i in range(n):
        result.append(a)
        a, b = b, a + b
    return result[-1]


#메모이제이션
memory = {1: 1, 2: 1}

def fibo_memoization(n):
    if n in memory:
        number = memory[n]
    else:
       number = fibo_memoization(n-1) + fibo_memoization(n-2)
       memory[n] = number
    return number


#제너레이터
#두번째로 빠른 방법이라고 한다
def fibo_generator(n):
    a, b = 1, 1
    for i in range(n):
        yield a
        a, b = b, a + b
    return a

#for x in fibo_generator(6):
#    print(x, end=' ')


#고유값
import numpy as np

def eigen_fib(n):
    F1 = np.array([[1, 1], [1, 0]])
    eigenvalues, eigenvectors = np.linalg.eig(F1)
    Fn = eigenvectors @ np.diag(eigenvalues ** n) @ eigenvectors.T
    return int(np.rint(Fn[0, 1]))


#행렬지수
#가장 빠른 방법이지만, 행렬 지수에 대한 이해가 필요
def multiply(a, b, x, y):
    return x*(a+b) + a*y, a*x + b*y

def square(a, b):
    a2 = a * a
    b2 = b * b
    ab = a * b
    return a2 + (ab << 1), a2 + b2

def power(a, b, m):
    if m == 0:
        return (0, 1)
    elif m == 1:
        return (a, b)
    else:
        x, y = a, b
        n = 2
        while n <= m:
            # repeated square until n = 2^q > m
            x, y = square(x, y)
            n = n*2
        # add on the remainder
        a, b = power(a, b, m-n//2)
        return multiply(x, y, a, b)

def implicit_fib(n):
    a, b = power(1, 0, n)
    return a
