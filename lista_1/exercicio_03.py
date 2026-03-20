#Exercício 3
'''3. Faça um programa que leia e valide as seguintes informações: 
a. Nome: maior que 3 caracteres; 
b. Idade: entre 0 e 150; 
c. Salário: maior que zero; 
d. Sexo: 'f' ou 'm'; 
e. Estado Civil: 's', 'c', 'v', 'd';'''

class CadastrarUsuario:
    def __init__(self, nome, idade, salario, sexo, estado_civil):
        self.nome = nome
        self.idade = idade
        self.salario = salario
        self.sexo = sexo
        self.estado_civil = estado_civil
        self.validar_entradas()

    def validar_entradas(self):
        try:
            is_valid = True
            if len(self.nome) < 3:
                print('Nome invalido, deve conter mais que 3 caracteres')
                is_valid = False

            if int(self.idade) < 0 or int(self.idade) > 150:
                print('Idade invalida, deve ser maior que 0 e menor que 150')
                is_valid = False

            if float(self.salario) < 0:
                print('Salário invalido, deve ser maior que 0')
                is_valid = False

            if self.sexo.lower() == 'm' or self.sexo.lower() == 'f':
                pass
            else:
                print('Sexo invalido, deve ser "m" ou "f"')
                is_valid = False

            if self.estado_civil.lower() == 's' or self.estado_civil.lower() == 'c' or self.estado_civil.lower() == 'v' or self.estado_civil.lower() == 'd':
                pass
            else:
                print('Estado civil invalido, deve ser "s", "c", "v" ou "d"')
                is_valid = False
            if is_valid:
                print('Usuário cadastrado com sucesso')
            else:
                print('Entradas incorretas, usuario não cadastrado')
        except:
            print('Entradas incorretas, usuario não cadastrado')
            
def main():
    nome = input('Digite seu nome: ')
    idade = input('Digite sua idade: ')
    salario = input('Digite seu salário: ')
    sexo = input('Digite seu sexo: f ou m: ')
    estado_civil = input('Digite seu estado civil: s, c, v, d: ')

    user_1 = CadastrarUsuario(nome, idade, salario, sexo, estado_civil)

if __name__ == '__main__':
    main()
