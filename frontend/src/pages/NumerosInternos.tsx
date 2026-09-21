import { useEffect, useRef, useState } from "react"
import {
  definirStatusNumeroInterno,
  excluirNumeroInterno, listarNumerosInternos,
} from "../services/numerosInternos"
import type { NumeroInterno } from "../services/numerosInternos"
import "../styles/urnas.css"
import "../styles/numeros-internos.css"

export default function NumerosInternos() {
  const [numeros, setNumeros] = useState<NumeroInterno[]>([])
  const [carregando, setCarregando] = useState(true)
  const [gravando, setGravando] = useState(false)
  const trava = useRef(false)
  const [erro, setErro] = useState("")
  const [erroLista, setErroLista] = useState("")
  const [sucesso, setSucesso] = useState("")
  const [revisao, setRevisao] = useState(0)
  const [exclusao, setExclusao] = useState<NumeroInterno | null>(null)

  useEffect(() => {
    let cancelado = false
    listarNumerosInternos().then(lista => {
      if (!cancelado) setNumeros(lista)
    }).catch(() => {
      if (!cancelado) setErroLista("Não foi possível carregar os números internos.")
    }).finally(() => {
      if (!cancelado) setCarregando(false)
    })
    return () => { cancelado = true }
  }, [revisao])

  function atualizarLista() {
    setErroLista("")
    setCarregando(true)
    setRevisao(valor => valor + 1)
  }

  async function executar(acao: () => Promise<void>, mensagem: string, erroPadrao: string) {
    if (trava.current) return
    trava.current = true
    setGravando(true)
    setErro("")
    setSucesso("")
    try {
      await acao()
      setSucesso(mensagem)
      atualizarLista()
    } catch {
      setErro(erroPadrao)
    } finally {
      trava.current = false
      setGravando(false)
    }
  }

  function alterarStatus(numero: NumeroInterno) {
    void executar(() => definirStatusNumeroInterno(numero.id, !numero.ativo),
      numero.ativo ? "Número desativado." : "Número ativado.",
      "Não foi possível alterar o status. Tente novamente.")
  }

  function confirmarExclusao() {
    if (!exclusao) return
    void executar(async () => {
      await excluirNumeroInterno(exclusao.id)
      setExclusao(null)
    }, "Número interno excluído.", "Não foi possível excluir o número. Tente novamente.")
  }

  const ocupado = gravando || carregando
  return (
    <div className="urnas-page numeros-internos">
      <header className="urnas-header">
        <div>
          <h1>Números internos</h1>
          <p>Telefones cadastrados como internos e ativos não recebem respostas automáticas do bot.</p>
        </div>
        <button className="btn-adicionar" onClick={() => { window.location.href = "/numeros-internos/novo" }}>
          + Novo número interno
        </button>
      </header>
      {erro && !exclusao && <p role="alert">{erro}</p>}
      {sucesso && <p role="status">{sucesso}</p>}
      <section className="urnas-table" aria-labelledby="numeros-titulo">
        <h2 id="numeros-titulo">Números cadastrados</h2>
        {carregando ? <p role="status">Carregando números...</p> : erroLista ? <p role="alert">{erroLista}</p> : numeros.length === 0 ? <p>Nenhum número interno cadastrado.</p> : (
          <div className="numeros-tabela">
            <table>
              <thead><tr><th>Nome</th><th>Telefone</th><th>Status</th><th>Ações</th></tr></thead>
              <tbody>{numeros.map(numero => (
                <tr key={numero.id}>
                  <td>{numero.nome}</td><td>{numero.telefone}</td><td>{numero.ativo ? "Ativo" : "Inativo"}</td>
                  <td><div className="numeros-acoes">
                    <button className="btn-editar" disabled={ocupado} onClick={() => alterarStatus(numero)}>{numero.ativo ? "Desativar" : "Ativar"}</button>
                    <button className="btn-remover" disabled={ocupado} onClick={() => { setErro(""); setExclusao(numero) }}>Excluir</button>
                  </div></td>
                </tr>
              ))}</tbody>
            </table>
          </div>
        )}
      </section>
      {exclusao && (
        <div className="modal-overlay">
          <div className="modal-confirm" role="dialog" aria-modal="true" aria-labelledby="excluir-interno-titulo">
            <h2 id="excluir-interno-titulo">Excluir número interno</h2>
            <p>Excluir o cadastro de {exclusao.nome} ({exclusao.telefone})? Esse telefone poderá voltar a receber respostas automáticas.</p>
            {erro && <p role="alert">{erro}</p>}
            <div className="modal-actions">
              <button className="btn-cancelar" disabled={gravando} onClick={() => { setExclusao(null); setErro("") }}>Cancelar</button>
              <button className="btn-remover" disabled={gravando} onClick={confirmarExclusao}>{gravando ? "Excluindo..." : "Confirmar exclusão"}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
