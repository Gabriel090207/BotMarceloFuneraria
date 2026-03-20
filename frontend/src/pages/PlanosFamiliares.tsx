import { useEffect, useMemo, useState } from "react"
import "../styles/planos.css"

import { collection, getDocs, addDoc, doc, updateDoc, deleteDoc } from "firebase/firestore"
import { db } from "../services/firebase"

type PlanoFamiliar = {
  id: string
  nome: string
  valor: number
  descricao: string
  ativo: boolean
}

type PlanoFormData = {
  nome: string
  valor: string
  descricao: string
  ativo: boolean
}

const formInicial: PlanoFormData = {
  nome: "",
  valor: "",
  descricao: "",
  ativo: true,
}

function formatarMoeda(valor: number): string {
  return valor.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  })
}

export default function PlanosFamiliares() {

  const [planos, setPlanos] = useState<PlanoFamiliar[]>([])
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState("")
  const [busca, setBusca] = useState("")

  const [modalAberto, setModalAberto] = useState(false)
  const [modoFormulario, setModoFormulario] = useState<"novo" | "editar">("novo")
  const [planoEditandoId, setPlanoEditandoId] = useState<string | null>(null)
  const [salvando, setSalvando] = useState(false)

  const [formData, setFormData] = useState<PlanoFormData>(formInicial)

  useEffect(() => {
    carregarPlanos()
  }, [])

  async function carregarPlanos() {
    try {

      const snapshot = await getDocs(collection(db, "planos_familiares"))

      const lista: PlanoFamiliar[] = []

      snapshot.forEach((docItem) => {
        lista.push({
          id: docItem.id,
          ...docItem.data()
        } as PlanoFamiliar)
      })

      setPlanos(lista)

    } catch (err) {
      console.error(err)
      setErro("Erro ao carregar planos")
    } finally {
      setCarregando(false)
    }
  }

  function abrirModalNovo() {
    setModoFormulario("novo")
    setPlanoEditandoId(null)
    setFormData(formInicial)
    setModalAberto(true)
  }

  function abrirModalEditar(plano: PlanoFamiliar) {
    setModoFormulario("editar")
    setPlanoEditandoId(plano.id)
    setFormData({
      nome: plano.nome,
      valor: String(plano.valor),
      descricao: plano.descricao,
      ativo: plano.ativo,
    })
    setModalAberto(true)
  }

  function fecharModal() {
    if (salvando) return
    setModalAberto(false)
    setPlanoEditandoId(null)
    setFormData(formInicial)
  }

  function atualizarCampo<K extends keyof PlanoFormData>(campo: K, valor: PlanoFormData[K]) {
    setFormData((prev) => ({ ...prev, [campo]: valor }))
  }

  async function salvarPlano(e: React.FormEvent) {
    e.preventDefault()

    setSalvando(true)

    const payload = {
      nome: formData.nome,
      valor: Number(formData.valor.replace(",", ".")),
      descricao: formData.descricao,
      ativo: formData.ativo,
    }

    try {

      if (modoFormulario === "novo") {

        const docRef = await addDoc(collection(db, "planos_familiares"), payload)

        setPlanos((prev) => [
          { id: docRef.id, ...payload },
          ...prev
        ])

      } else if (planoEditandoId) {

        await updateDoc(doc(db, "planos_familiares", planoEditandoId), payload)

        setPlanos((prev) =>
          prev.map((p) =>
            p.id === planoEditandoId ? { id: p.id, ...payload } : p
          )
        )

      }

      fecharModal()

    } catch (err) {
      console.error(err)
      alert("Erro ao salvar plano")
    } finally {
      setSalvando(false)
    }
  }

  async function removerPlano(id: string) {
    if (!confirm("Remover plano?")) return

    try {

      await deleteDoc(doc(db, "planos_familiares", id))

      setPlanos((prev) => prev.filter((p) => p.id !== id))

    } catch (err) {
      console.error(err)
      alert("Erro ao remover plano")
    }
  }

  async function alternarStatus(plano: PlanoFamiliar) {

    const novoStatus = !plano.ativo

    try {

      await updateDoc(doc(db, "planos_familiares", plano.id), {
        ativo: novoStatus
      })

      setPlanos((prev) =>
        prev.map((p) =>
          p.id === plano.id ? { ...p, ativo: novoStatus } : p
        )
      )

    } catch (err) {
      console.error(err)
      alert("Erro ao atualizar status")
    }
  }

  const planosFiltrados = useMemo(() => {
    return planos.filter((p) =>
      p.nome.toLowerCase().includes(busca.toLowerCase())
    )
  }, [planos, busca])

  return (
    <div className="planos-page">

      <div className="planos-header">
        <div>
          <h1>Planos Familiares</h1>
          <p className="planos-subtitle">
            Gerencie os planos do sistema
          </p>
        </div>

        <button className="btn-adicionar" onClick={abrirModalNovo}>
          Novo Plano
        </button>
      </div>

      <div className="planos-toolbar">
        <input
          placeholder="Buscar plano..."
          value={busca}
          onChange={(e) => setBusca(e.target.value)}
          className="planos-busca"
        />
      </div>

      {erro && <div className="planos-alerta-erro">{erro}</div>}

      <div className="planos-table">

        {carregando ? (
          <div className="planos-loading">Carregando...</div>
        ) : planosFiltrados.length === 0 ? (
          <div className="planos-vazio">Nenhum plano</div>
        ) : (
          <table>

            <thead>
              <tr>
                <th>Plano</th>
                <th>Descrição</th>
                <th>Valor</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>

            <tbody>

              {planosFiltrados.map((plano) => (

                <tr key={plano.id}>
                  <td>{plano.nome}</td>
                  <td>{plano.descricao}</td>
                  <td>{formatarMoeda(plano.valor)}</td>

                  <td>
                    <span className={plano.ativo ? "status-ativo" : "status-inativo"}>
                      {plano.ativo ? "Ativo" : "Inativo"}
                    </span>
                  </td>

                  <td>
                    <div className="plano-acoes">

                      <button className="btn-editar" onClick={() => abrirModalEditar(plano)}>
                        Editar
                      </button>

                      <button className="btn-status" onClick={() => alternarStatus(plano)}>
                        {plano.ativo ? "Desativar" : "Ativar"}
                      </button>

                      <button className="btn-remover" onClick={() => removerPlano(plano.id)}>
                        Remover
                      </button>

                    </div>
                  </td>

                </tr>

              ))}

            </tbody>

          </table>
        )}

      </div>

      {modalAberto && (
        <div className="modal-overlay" onClick={fecharModal}>
          <div className="modal-plano" onClick={(e) => e.stopPropagation()}>

            <h2>{modoFormulario === "novo" ? "Novo Plano" : "Editar Plano"}</h2>

            <form onSubmit={salvarPlano} className="modal-form">

              <input
                placeholder="Nome"
                value={formData.nome}
                onChange={(e) => atualizarCampo("nome", e.target.value)}
              />

              <input
                placeholder="Valor"
                value={formData.valor}
                onChange={(e) => atualizarCampo("valor", e.target.value)}
              />

              <textarea
                placeholder="Descrição"
                value={formData.descricao}
                onChange={(e) => atualizarCampo("descricao", e.target.value)}
              />

              <label>
                <input
                  type="checkbox"
                  checked={formData.ativo}
                  onChange={(e) => atualizarCampo("ativo", e.target.checked)}
                />
                Ativo
              </label>

              <div className="modal-acoes">
                <button type="button" onClick={fecharModal}>
                  Cancelar
                </button>

                <button type="submit">
                  {salvando ? "Salvando..." : "Salvar"}
                </button>
              </div>

            </form>

          </div>
        </div>
      )}

    </div>
  )
}