import { useRef, useState } from "react"
import type { FormEvent } from "react"
import { FiCheck } from "react-icons/fi"
import { cadastrarNumeroInterno, CadastroNumeroError } from "../services/numerosInternos"
import { normalizarTelefoneBrasileiro } from "../utils/telefoneBrasileiro"
import "../styles/nova-urna.css"
import "../styles/numeros-internos.css"

export default function NovoNumeroInterno() {
  const [nome, setNome] = useState("")
  const [telefone, setTelefone] = useState("")
  const [salvando, setSalvando] = useState(false)
  const [sucesso, setSucesso] = useState(false)
  const [erro, setErro] = useState("")
  const trava = useRef(false)

  async function cadastrar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault()
    if (trava.current) return
    if (!telefone.trim()) {
      setErro("Informe o telefone.")
      return
    }
    if (!normalizarTelefoneBrasileiro(telefone)) {
      setErro("Informe um telefone válido.")
      return
    }
    trava.current = true
    setSalvando(true)
    setErro("")
    try {
      await cadastrarNumeroInterno(nome, telefone)
      setNome("")
      setTelefone("")
      setSucesso(true)
    } catch (falha) {
      // A listagem agora está em outra página; mantenha a mensagem coerente.
      setErro(falha instanceof CadastroNumeroError
        ? falha.message.replace("Consulte a lista abaixo.", "Consulte a página de Números internos.")
        : "Não foi possível cadastrar o número. Tente novamente.")
    } finally {
      trava.current = false
      setSalvando(false)
    }
  }

  return (
    <div className="nova-urna-page numeros-internos">
      <h1>Novo número interno</h1>
      <form className="nova-urna-form" onSubmit={cadastrar} noValidate>
        <div className="nova-urna-grid">
          <div className="nova-urna-field">
            <label htmlFor="interno-nome">Nome (opcional)</label>
            <input id="interno-nome" value={nome} onChange={e => setNome(e.target.value)} disabled={salvando} />
          </div>
          <div className="nova-urna-field">
            <label htmlFor="interno-telefone">Telefone com DDD</label>
            <input id="interno-telefone" type="tel" value={telefone} onChange={e => setTelefone(e.target.value)} required disabled={salvando} aria-describedby="telefone-ajuda" />
            <small id="telefone-ajuda">Informe DDD e telefone, com ou sem +55, espaços, parênteses e hífen.</small>
          </div>
        </div>
        {erro && <p role="alert">{erro}</p>}
        <button className="btn-salvar" type="submit" disabled={salvando || sucesso}>{salvando ? "Salvando..." : "Salvar número interno"}</button>
      </form>
      {sucesso && (
        <div className="modal-overlay">
          <div className="modal-sucesso" role="dialog" aria-modal="true" aria-labelledby="cadastro-interno-sucesso">
            <FiCheck className="modal-icon" />
            <h2 id="cadastro-interno-sucesso">Número interno criado com sucesso</h2>
            <button onClick={() => setSucesso(false)}>OK</button>
          </div>
        </div>
      )}
    </div>
  )
}
