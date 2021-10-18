from flask import Flask,jsonify
from flask import request
from flask import render_template


from datetime import date

import sqlite3
from sqlite3 import Error


#######################################################
# Instancia da Aplicacao Flask

app = Flask(__name__)


#######################################################
# 1. Cadastrar produtos

@app.route('/produtos/cadastrar', methods=['GET', 'POST'])

def cadastrar():

    if request.method == 'POST':

        descricao = request.form['descricao']
        precocompra = request.form['precocompra']
        precovenda = request.form['precovenda']
        datacriacao = date.today()

        mensagem = 'Erro - não cadastrado'

        if descricao and precocompra and precovenda and datacriacao:
            registro = (descricao, precocompra, precovenda, datacriacao)

            try:
                conn = sqlite3.connect('database/db-produtos.db')

                sql = ''' INSERT INTO produtos(descricao, precocompra, precovenda, datacriacao)
                              VALUES(?,?,?,?) '''

                cur = conn.cursor()

                cur.execute(sql, registro)

                conn.commit()

                mensagem = 'Sucesso - cadastrado'

            except Error as e:
                print(e)
            finally:
                conn.close()

    return render_template('cadastrar.html')


#######################################################
# 2. Listar produtos

@app.route('/produtos/listar', methods=['GET'])

def listar():
    try:
        conn = sqlite3.connect('database/db-produtos.db')

        sql = '''SELECT * FROM produtos'''

        cur = conn.cursor()

        cur.execute(sql)

        registros = cur.fetchall()

        return render_template('listar.html', regs=registros)

    except Error as e:
        print(e)
    finally:
        conn.close()


#######################################################
# 3. Excluir produtos
@app.route('/produtos/excluir', methods=['GET', 'POST'])

def excluir():

    if request.method == 'POST':

        excluir = request.form['idproduto']

        mensagem = 'Erro - não excluído'

        if excluir:
            registro = excluir
            try:
                conn = sqlite3.connect('database/db-produtos.db')

                sql = '''DELETE FROM produtos WHERE idproduto = ?'''

                cur = conn.cursor()

                cur.execute(sql, registro)

                conn.commit()

                mensagem = 'Sucesso - excluído'

            except Error as e:
                print(e)
            finally:
                conn.close()

    return render_template('excluir.html')


#######################################################
# 4. alterar produtos
@app.route('/produtos/alterar', methods=['GET', 'POST'])

def alterar():

    if request.method == 'POST':

        descricao = request.form['descricao']
        precocompra = request.form['precocompra']
        precovenda = request.form['precovenda']
        codproduto = request.form['idproduto']

        mensagem = 'Erro - não alterado'

        if codproduto and descricao and precocompra and precovenda:
            registro = (descricao, precocompra, precovenda, codproduto)

            try:
                conn = sqlite3.connect('database/db-produtos.db')

                sql = '''UPDATE produtos 
                SET descricao = ?, precocompra = ?, precovenda = ?
                WHERE idproduto = ?'''

                cur = conn.cursor()

                cur.execute(sql, registro)

                conn.commit()

                mensagem = 'Sucesso - alterado'

            except Error as e:
                print(e)
            finally:
                conn.close()

    return render_template('alterar.html')

#######################################################
# Rota de Erro

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404



#######################################################
# Execucao da Aplicacao

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)