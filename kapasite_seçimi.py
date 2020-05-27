from __future__ import print_function
from ortools.linear_solver import pywraplp

def veri_olusturma():
    data = {}

    data["c_ij"] = [
        [211, 232, 238, 299],
        [232, 212, 230, 280],
        [240, 230, 215, 270],
        [300, 280, 270, 225],
    ]

    data["d_i"] = [120, 170, 180, 150]

    data["dk_j"] = [8, 9.5, 5.6, 6.1]

    data["yk_j"] = [9, 11, 9.3, 10.2]
    data["i"] = 4
    data["j"] = 4
    
    return data

def main():
    data = veri_olusturma()

    i_r = data["i"]
    j_r = data["j"]
    #çözücü tanımlama
    solver = pywraplp.Solver("ENM444 Arasınav Modeli",
        pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    inf = solver.infinity()

    x, y, z = {}, {}, {}
    #karar değişkenlerini oluşturma
    for i in range(1,i_r + 1):
        for j in range(1,j_r + 1):
            x[i, j] = solver.IntVar(0, inf, 'x[%i, %i]' % (i, j))

    for j in range(1, j_r + 1):
        y[j] = solver.BoolVar("y[%i]"%j)

    for j in range(1, j_r + 1):
        z[j] = solver.BoolVar("z[%i]"%j)

    # kısıtları oluşturma

    for i in range(1, i_r + 1):
        solver.Add(solver.Sum([x[i,j] for j in range(1, j_r + 1)])>=data["d_i"][i-1])

    for j in range(1, j_r + 1):
        solver.Add(solver.Sum([x[i, j] for i in range(1, i_r + 1)])<=200*y[j]+400*z[j])

    for j in range(1, j_r + 1):
        solver.Add(y[j] + z[j] <= 1)

    #-------------- kısıtlar bitti --------------------
    
    #-------------- oobjective func yazımı ------------

    solver.Minimize(solver.Sum([data["dk_j"][j-1]*y[j] for j in range(1, j_r + 1)]) +
    solver.Sum([data["yk_j"][j-1]*z[j] for j in range(1, j_r + 1)])+
    solver.Sum([data["c_ij"][i-1][j-1]*x[i, j] for i in range(1, i_r + 1) for j in range(1, j_r + 1)])
    )     

    solver.Solve()
    print("*********************** ÇÖZÜM RAPORU ***********************\n")
    print("\t\t Toplam Maliyet = ", str(solver.Objective().Value())," TL.\n")
    print("------------------ Fabrikaların Açıldığı Şehirler ------------------\n")
    print("   ############# 200 bin Kapasiteli Fabrikalar #############\n")
    for j in range(1, j_r + 1):
        print("\t\t",y[j].name()," = ", y[j].solution_value())
    print("\n   ############# 400 bin Kapasiteli Fabrikalar #############\n")
    for j in range(1, j_r + 1):
        print("\t\t",z[j].name()," = ", z[j].solution_value())
    
    print("\n------------------ Bölgeler ve Şehirler Arasındaki Ürün Gönderimi ------------------\n")
    for i in range(1, i_r + 1):
        for j in range(1, j_r + 1):
            print("\t\t",x[i,j].name(), " = ", x[i,j].solution_value())
    print("\n---------------------------------------------------------------------------------------\n")
    print('Problem  %f millisaniyede çözüldü' % solver.wall_time())

if __name__ == '__main__':
  main()