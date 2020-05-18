from __future__ import print_function
from ortools.linear_solver import pywraplp

def veri_oluşturma():
    #veri çekmek için kullanacağım
    data = {}

    data["cost"] = [
        [150,250,200,25],
        [150,250,200,75],
        [75,200,150,125],
        [150,200,125,125],
        [100,200,125,150],
        [175,175,125,125],
        [150,175,100,150],
        [150,150,100,200],
        [75,200,100,250],
        [150,125,25,250],
        [125,125,75,300],
        [300,200,150,200],
        [300,175,125,200],
        [250,100,125,250],
        [250,75,75,300],
        [250,25,125,300],
    ]

    data["talepler"] = [40,35,100,25,40,25,50,30,50,65,40,30,20,30,40,55]
    data["sabit_maliyetler"] = [165428,131230,140000,145000]
    data["i"] = 16
    data["j"] = 4
    data["#_of_constraints"] = 4
    return data

def main():
    data = veri_oluşturma()
    solver = pywraplp.Solver("ENM444 KS3 modeli",
    pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    infinity = solver.infinity()

    x ={}
    y ={}
    z ={}
    # x değerini tanımlayalım integer olduğu için IntVar kullanıcaz

    for i in range(data["i"]):
        for j in range(data["j"]):
            x[i, j] = solver.IntVar(0, infinity, 'x[%i, %i]' % (i, j))

    for j in range(data["j"]):
        y[j] = solver.BoolVar("y[%i]"%j)
    for j in range(data["j"]):
        z[j] = solver.IntVar(0,infinity, "z[%i]" % j)

    for j in range(data["j"]):
        solver.Add(z[j] <= 10*y[j])
    
    for j in range(data["j"]):
        solver.Add(solver.Sum([x[i,j] for i in range(data["i"])])<= z[j]*25)

    for i in range(data["i"]):
        solver.Add(data["talepler"][i]<=solver.Sum(x[i,j] for j in range(data["j"])))
    for i in range(data["i"]):
        for j in range(data["j"]):
            solver.Add(x[i,j]<=1000*y[j])

    solver.Minimize(solver.Sum([data["sabit_maliyetler"][j]*y[j] for j in range(data["j"])]) + solver.Sum([data["cost"][i][j]*x[i,j] for i in range(data["i"]) for j in range(data["j"])]))

    sol = solver.Solve()
    print("*********************** ÇÖZÜM RAPORU ***********************")
    print("Toplam Maliyet : ", solver.Objective().Value())
    print("\n ------------------ Açılan Ofisler ------------------")
    for j in range(data["j"]):
        print(y[j].name()," = ", y[j].solution_value())
    
    print("\n ------------------ Ofisler ile Şehirler Arasındaki Seyehat Sayısı ------------------")
    
    for i in range(data["i"]):
        for j in range(data["j"]):
            print(x[i,j].name(), " = ", x[i,j].solution_value())
    
    print("\n ------------------ Ofislerdeki Danışman Sayısı ------------------")

    for j in range(data["j"]):
        print(z[j].name()," = ", z[j].solution_value())

    print('Problem  %f millisaniyede çözüldü' % solver.wall_time())

if __name__ == '__main__':
  main()