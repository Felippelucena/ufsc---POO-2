#Exercício 2
'''2. Faça um programa que leia um nome de usuário e a sua senha e não aceite a senha igual 
ao nome do usuário, mostrando uma mensagem de erro e voltando a pedir as informações. '''

def login(usuario, senha):
    is_login = False
    while is_login == False:
        if usuario == senha:
            print('Usuario e senha não podem ser iguais')
            usuario = input('Digite seu nome de usuario: ')
            senha = input('Digite sua senha: ')
        else:
            is_login = True
    print('Login realizado com sucesso')

if __name__ == '__main__':
    login(input('Digite seu nome de usuario: '), input('Digite sua senha: '))
