# Trabalho de Modelagem de Sistemas - SP Mulher Segura
# 2°A informática
# Programação Orientada a Objeto 
# Alunos
# Maria Luiza 
# Marcos Cezar 
# Guilherme
# Anna lídia
# Joaquim Lucas

# obssss: os relacionamentos (herança, composição, agregação e associação) estão comentados em cima da linha onde acontecem

from datetime import datetime, date


class Pessoa:
    def __init__(self, nomecompleto, cpf, datanascimento, telefone):
        self.nomecompleto = nomecompleto
        self.cpf = cpf
        self.datanascimento = datanascimento
        self.telefone = telefone

        # composição, a Pessoa que cria os contatos de emergência dela
        self.contatos_emergencia = []

    def cadastrar(self):
        print(f"Cadastrando {self.nomecompleto}, CPF {self.cpf}")
        return True

    def desativarConta(self):
        print(f"Conta de {self.nomecompleto} desativada")
        return True

    def adicionar_contato_emergencia(self, email):
        # composição aqui, quem cria o objeto é a própria Pessoa
        contato = ContatoEmergencia(email)
        self.contatos_emergencia.append(contato)
        contato.adicionar()
        return contato

    def __str__(self):
        return f"{self.nomecompleto} ({self.cpf})"


class ContatoEmergencia:
    def __init__(self, email):
        self.email = email
        self.ativo = False

    def adicionar(self):
        print(f"contato {self.email} adicionado")
        return True

    def editar(self):
        print(f"editando contato {self.email}")

    def ativar(self):
        self.ativo = True
        print(f"contato {self.email} ativado")
        return True

    def desativar(self):
        self.ativo = False
        print(f"contato {self.email} desativado")
        return True


class BoletimOcorrencia:
    lista_boletins = []  # pra dar pra usar no consultar()

    def __init__(self, idboletim, tipoocorrencia, dataocorrencia, localocorrencia, nomeagressor, descricao):
        self.idboletim = idboletim
        self.tipoocorrencia = tipoocorrencia
        self.dataocorrencia = dataocorrencia
        self.localocorrencia = localocorrencia
        self.nomeagressor = nomeagressor
        self.status = "Aberto"
        self.descricao = descricao
        self.documentos = []

        # associação com MedidaProtetiva 
        self.medidas_protetivas = []

    def registrar(self):
        BoletimOcorrencia.lista_boletins.append(self)
        print(f"boletim {self.idboletim} ({self.tipoocorrencia}) registrado")
        return True

    def editar(self):
        print(f"editando boletim {self.idboletim}")

    def anexarDocumento(self):
        doc = f"doc_{len(self.documentos)+1}.pdf"
        self.documentos.append(doc)
        print(f"documento {doc} anexado no boletim {self.idboletim}")

    @staticmethod
    def consultar(idboletim):
        for b in BoletimOcorrencia.lista_boletins:
            if b.idboletim == idboletim:
                return b
        print("boletim não encontrado")
        return None

    def vincular_medida(self, medida):
        # associação do BoletimOcorrencia com MedidaProtetiva
        self.medidas_protetivas.append(medida)
        medida.boletins.append(self)


class MedidaProtetiva:
    def __init__(self, nomeagressor, datainicio, datafim):
        self.nomeagressor = nomeagressor
        self.datainicio = datainicio
        self.datafim = datafim
        self.status = "Pendente"
        self.boletins = []  # associação com BoletimOcorrencia

    def cadastrar(self):
        self.status = "Ativa"
        print(f"medida protetiva contra {self.nomeagressor} cadastrada")
        return True

    def editar(self):
        print(f"editando medida protetiva contra {self.nomeagressor}")


class BotaoPanico:
    def __init__(self, codigodispositivo):
        self.codigodispositivo = codigodispositivo
        self.status = "Inativo"
        self.ultimaativacao = None

        # composição com Notificacao, o botão que gera a notificação quando ligado
        self.notificacoes = []

    def acionar(self):
        self.status = "Acionado"
        self.ultimaativacao = datetime.now()
        print(f"botão {self.codigodispositivo} ACIONADO!!! mandando alerta")
        notif = Notificacao()  # composição, a notificação ocorre aqui 
        notif.enviarNotificacao()
        self.notificacoes.append(notif)
        return True

    def obterLocalizacao(self):
        print("pegando localização do gps...")
        return "localização obtida"

    def verificarBateria(self):
        print("checando bateria")
        return 85

    def desativar(self):
        self.status = "Inativo"
        print(f"botão {self.codigodispositivo} desativado")
        return True


class Notificacao:
    todas = []

    def __init__(self):
        self.dataHora = datetime.now()

    def enviarNotificacao(self):
        Notificacao.todas.append(self)
        print(f"notificação enviada as {self.dataHora.strftime('%H:%M:%S')}")
        return "enviada"

    def confirmarRecebimento(self):
        print("recebimento confirmado")
        return True

    @staticmethod
    def listarNotificacoes():
        return Notificacao.todas


class ServicoProtecao:
    def __init__(self, tipo, telefone, endereco):
        self.tipo = tipo
        self.telefone = telefone
        self.endereco = endereco

        # associação com Notificacao e com Usuario
        self.notificacoes = []
        self.usuarios = []

    def cadastrarServico(self):
        print(f"serviço {self.tipo} cadastrado, tel {self.telefone}")
        return True

    def consultarDisponibilidade(self):
        print(f"consultando disponibilidade do {self.tipo}")
        return True

    def vincularUsuario(self, usuario):
        # associação ServicoProtecao e Usuario
        self.usuarios.append(usuario)
        usuario.servicos_protecao.append(self)
        print(f"usuario {usuario.nomecompleto} vinculado ao serviço {self.tipo}")
        return True

    def receber_notificacao(self, notif):
        # associação ServicoProtecao e Notificacao
        self.notificacoes.append(notif)
        print(f"{self.tipo} recebeu uma notificação")


class Atendimento:
    def __init__(self, id, tipo):
        self.id = id
        self.dataHora = datetime.now()
        self.tipo = tipo
        self.status = "Pendente"

    def iniciarAtendimento(self):
        self.status = "Em andamento"
        print(f"atendimento {self.id} ({self.tipo}) iniciado")

    def encerrarAtendimento(self):
        self.status = "Encerrado"
        print(f"atendimento {self.id} encerrado")

    def atualizarStatus(self):
        print(f"status do atendimento {self.id}: {self.status}")


class Delegacia:
    def __init__(self, nome, endereco, telefone):
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone

        # associação BoletimOcorrencia e MedidaProtetiva
        self.ocorrencias = []
        self.medidas = []

        # agregação com ServicoProtecao, os serviços existem independente da delegacia
        self.servicos_protecao = []

    def consultarOcorrencias(self):
        print(f"consultando ocorrências da {self.nome}")
        return self.ocorrencias

    def encaminharMedidaProtetiva(self, medida):
        self.medidas.append(medida)
        medida.status = "Encaminhada"
        print(f"medida contra {medida.nomeagressor} encaminhada pela {self.nome}")

    def receber_ocorrencia(self, boletim):
        self.ocorrencias.append(boletim)
        print(f"boletim {boletim.idboletim} recebido na {self.nome}")

    def agregar_servico(self, servico):
        # agregação
        self.servicos_protecao.append(servico)
        print(f"serviço {servico.tipo} agregado a delegacia {self.nome}")


# subclasses de Pessoa (herança)

class Usuario(Pessoa):
    def __init__(self, nomecompleto, cpf, datanascimento, telefone, numerogov, endereco, senha):
        super().__init__(nomecompleto, cpf, datanascimento, telefone)  # herança, chamando o construtor da Pessoa

        self.numerogov = numerogov
        self.endereco = endereco
        self.senha = senha

        # agregação com BotaoPanico 
        self.botao_panico = None

        # associações
        self.boletins = []
        self.medidas_protetivas = []
        self.atendimentos = []
        self.servicos_protecao = []

    def editarDados(self):
        print(f"editando dados de {self.nomecompleto}")

    def atualizarLocalizacao(self):
        print(f"atualizando localização de {self.nomecompleto}")
        return self.endereco

    def alterarSenha(self):
        print(f"senha de {self.nomecompleto} alterada")
        return True

    def vincular_botao_panico(self, botao):
        # agregação Usuario e BotaoPanico
        self.botao_panico = botao
        print(f"botão {botao.codigodispositivo} vinculado a {self.nomecompleto}")

    def registrar_boletim(self, boletim):
        self.boletins.append(boletim)
        boletim.registrar()

    def solicitar_medida_protetiva(self, medida):
        self.medidas_protetivas.append(medida)
        medida.cadastrar()

    def solicitar_atendimento(self, atendimento):
        self.atendimentos.append(atendimento)
        atendimento.iniciarAtendimento()


class AgentePolicial(Pessoa):
    def __init__(self, nomecompleto, cpf, datanascimento, telefone, matricula, cargo, delegacia):
        super().__init__(nomecompleto, cpf, datanascimento, telefone)  # herança de novo

        self.matricula = matricula
        self.cargo = cargo

        # agregação com Delegacia, ela existe independente do agente
        self.delegacia = delegacia

        self.atendimentos = []
        self.ocorrencias_atendidas = []

    def atenderOcorrencia(self, boletim):
        self.ocorrencias_atendidas.append(boletim)
        boletim.status = "Em atendimento"
        print(f"agente {self.nomecompleto} atendendo o boletim {boletim.idboletim}")
        self.delegacia.receber_ocorrencia(boletim)  # usando a agregação com a delegacia

    def realizar_atendimento(self, atendimento):
        self.atendimentos.append(atendimento)
        atendimento.iniciarAtendimento()


# teste (fiquei meio em dúvida nessa parte prof)

if __name__ == "__main__":

    print("### testando cada classe ###\n")

    p = Pessoa("Malu do grau", "676.767.676-67", date(2007, 6, 7), "676796767676")
    p.cadastrar()
    p.adicionar_contato_emergencia("contato@email.com")

    c = ContatoEmergencia("emergencia@email.com")
    c.adicionar()
    c.ativar()

    b = BoletimOcorrencia(1, "Ameaça", date(2026, 6, 7), "Rua aura, 67", "Fulano", "descrição teste")
    b.registrar()
    b.anexarDocumento()
    BoletimOcorrencia.consultar(1)

    m = MedidaProtetiva("Anna Lendea", date(2026, 6, 7), date(2026, 12, 5))
    m.cadastrar()

    bp = BotaoPanico(555)
    bp.acionar()
    bp.verificarBateria()

    sp = ServicoProtecao("SAMU", "192", "Central SP")
    sp.cadastrarServico()
    sp.consultarDisponibilidade()

    at = Atendimento(1, "Emergência")
    at.iniciarAtendimento()
    at.atualizarStatus()
    at.encerrarAtendimento()

    dl = Delegacia("1ª DDM", "Av. Central, 6767", "1123456789")
    dl.consultarOcorrencias()

    u = Usuario("Ana Silva", "222.222.222-22", date(1995, 6, 7), "11988887777", 12345, "Rua das Flores, 42", "123")
    u.cadastrar()
    u.editarDados()
    u.alterarSenha()

    ag = AgentePolicial("João Souza", "333.333.333-33", date(1985, 6, 7), "1133334444", 987, "Investigador", dl)
    ag.cadastrar()

    print("\n### agora testando tudo junto (fluxo completo) ###\n")

    delegacia = Delegacia("5ª DDM", "Rua da Justiça, 667", "1132165498")
    samu = ServicoProtecao("SAMU", "192", "Central SAMU")
    pm = ServicoProtecao("Policia Militar", "190", "Central PM")

    delegacia.agregar_servico(samu)
    delegacia.agregar_servico(pm)

    agente = AgentePolicial("Marcelina", "444.444.444-44", date(1988, 11, 2), "1199998888", 456, "Delegada", delegacia)

    usuaria = Usuario("Lorenão", "555.555.555-55", date(1992, 1, 30), "11977776666", 67890, "Av. Paulista, 900", "senha123")
    usuaria.cadastrar()
    usuaria.adicionar_contato_emergencia("mae.beatriz@email.com")

    botao = BotaoPanico(101)
    usuaria.vincular_botao_panico(botao)
    samu.vincularUsuario(usuaria)

    print("\nemergência acontecendo")
    usuaria.botao_panico.acionar()
    ultima_notif = usuaria.botao_panico.notificacoes[-1]
    samu.receber_notificacao(ultima_notif)

    print("\nregistrando ocorrência")
    boletim = BoletimOcorrencia(2, "Violência doméstica", date(2026, 9, 10), "Rua das Acácias, 67", "Agressor beta", "relato da ocorrência")
    usuaria.registrar_boletim(boletim)
    agente.atenderOcorrencia(boletim)

    medida = MedidaProtetiva("Agressor beta", date(2026, 9, 11), date(2026, 12, 11))
    usuaria.solicitar_medida_protetiva(medida)
    boletim.vincular_medida(medida)
    delegacia.encaminharMedidaProtetiva(medida)

    atendimento = Atendimento(10, "Acolhimento psicológico")
    usuaria.solicitar_atendimento(atendimento)
    agente.realizar_atendimento(atendimento)
    atendimento.encerrarAtendimento()

    print("\nSP MULHER SEGURA")
    print("usuária:", usuaria)
    print("contatos de emergência:", [ct.email for ct in usuaria.contatos_emergencia])
    print("boletins da usuária:", [bo.idboletim for bo in usuaria.boletins])
    print("medidas protetivas:", [md.nomeagressor for md in usuaria.medidas_protetivas])
    print("serviços vinculados:", [s.tipo for s in usuaria.servicos_protecao])
    print("agente responsável:", agente.nomecompleto, "- delegacia:", agente.delegacia.nome)
    print("ocorrências na delegacia:", [bo.idboletim for bo in delegacia.ocorrencias])
    print("serviços da delegacia:", [s.tipo for s in delegacia.servicos_protecao])