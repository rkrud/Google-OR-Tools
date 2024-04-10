import ortools
from ortools.linear_solver import pywraplp # pywraplp: 선형 프로그래밍 문제를 해결하는데 필요한 함수와 클래스들을 제공

solver = solver = pywraplp.Solver.CreateSolver('SCIP')

# Set/Parameters

data = {}
values = [48, 30, 42, 36, 22, 43, 18, 24, 36, 29, 30, 25, 19, 41, 34, 32, 27, 24, 18]
weights = [10, 30, 12, 22, 12, 20, 9, 9, 18, 20, 25, 18, 7, 16, 24, 21, 21, 32, 9]
volume = [15, 20, 18, 20, 5, 12, 7, 7, 24, 30, 25, 20, 5, 25, 19, 24, 19, 14, 30]
rad = [3, 1, 2, 3, 1, 2, 0, 2, 2, 1, 2, 3, 4, 3, 2, 3, 1, 1, 3]
assert len(values) == len(weights) == len(volume) == len(rad)
data['values'] = values
data['weights'] = weights
data['volume'] = volume
data['rad'] = rad
data['items'] = list(range(len(weights))) # 아이템에 인덱스 부여
data['num_items'] = len(values) # 총 아이템 개수
number_bags = 5 #All have the same capacity of 50 pounds
data['bag_capacities'] = [50, 50, 50, 50, 50] #pounds (무게)
data['bag_volume'] = [50,50,50,50,50] #while this equals bag_capacities, I made it its own variable in case (부피)
data['rad_capacities'] = [5,5,5,5,5] # 방사능
#I wanted to change the values at a later data
data['bags'] = list(range(number_bags)) # 가방에 인덱스 부여
assert len(data['bag_capacities']) == number_bags
assert len(data['bag_capacities']) == len(data['bag_volume']) == len(data['rad_capacities'])
print("Values: ",*data['values'])
print('Weights:',*data['weights'])
print('Volume:',*data['volume'])
print('Radiation Levels:', *data['rad'])
print("Number of Items:", data['num_items'])
print("Number of Knapsacks:" , number_bags)
print('Knapsack Capacities: 50 Pounds, 50 cubic inches, 5 Levels of Radiation')

# Decision variables (결정변수)
# 아이템 i가 가방 j에 포함되면 1, 안되면 0 

x = {}
for i in data['items']:
    for j in data['bags']:
        x[(i,j)] = solver.IntVar(0,1,'x_%i_%i' % (i, j)) #solver.IntVar는 google ORTools의 선형 프로그래밍 솔버를 위한 정수형 변수를 생성하는 메서드, 변수명: x_i_j 형태

#constraints
        
#Constraint for an item being placed in 1 knapsack (각 item은 하나의 가방에만 있을 수 있다)
for i in data['items']:
    solver.Add(sum(x[i,j] for j in data['bags'])<=1)
#Knapsack Capacity Constraint(각 가방의 무게는 50파운드를 초과할 수 없다)
for j in data['bags']:
    solver.Add(sum(x[(i,j)]*data['weights'][i] 
                  for i in data['items']) <= data['bag_capacities'][j])
#Volume Constraint (각 가방의 부피는 50입방인치를 초과할 수 없다.)
for j in data['bags']:
    solver.Add(sum(x[(i,j)]*data['volume'][i] # . Add : 선형 최적화 문제에서 제약 조건을 추가하는 메서드
                  for i in data['items']) <= data['bag_volume'][j])
#Radiation Constraint(각 가방의 방사능은 5 래드를 초과할 수 없다)
for j in data['bags']:
    solver.Add(sum(x[(i,j)]*data['rad'][i]
                    for i in data['items']) <= data['rad_capacities'][j])
    
#objective function
    
objective = solver.Objective() # .Objective: 최적화 문제에서 사용할 목적 함수를 생성
for i in data['items']:
    for j in data['bags']:
        objective.SetCoefficient(x[(i,j)], data['values'][i]) 
        # SetCoefficien: 일반적으로 선형 제약 조건을 설정할 때 사용, 변수와 해당 변수의 계수를 설정
        # x[(i,j)]는 변수, data['values'][i]는 해당 변수의 계수로 설정
objective.SetMaximization()

# solve 
solv = solver.Solve() #최적화 문제를 해결하는 메서드
if solv == pywraplp.Solver.OPTIMAL:
    print("-------------------------solve------------------------------------------")
    print('Total Packed Value:', objective.Value()) # .Value : 최적화 문제의 목적 함수의 값, 즉 최적해에서의 목적 함수의 값을 반환하는 메서드
    total_weight = 0
    for j in data['bags']:
        bag_value = 0
        bag_weight = 0
        bag_volume= 0
        bag_rad = 0
        print('\n','Bag', j+1 , '\n')
        for i in data['items']:
            if x[i,j].solution_value()>0: # .solution_value : 해당 변수가 최적해에서 어떤 값을 가지는지를 반환하는 메서드 ,해당 항목이 해당 가방에 포함되어 있는지 확인할 수 있음
                print('Item:', i , 
                      'value',data['values'][i],
                      'Weight', data['weights'][i], 
                      'Volume',data['volume'][i],
                      'Radiation', data['rad'][i]
                     )
                bag_value += data['values'][i]
                bag_weight += data['weights'][i]
                bag_volume += data['volume'][i]
                bag_rad += data['rad'][i]
        print('Packed Knapsack Value: ', bag_value)
        print('Packed Knapsack Weight: ', bag_weight)
        print('Packed Knapsack Volume: ', bag_volume)
        print('Pack Knapsack Radiation: ', bag_rad)
else:
    print("There is no optimal solution")