import { useEffect, useMemo, useState } from "react"
import "../styles/planos.css"

import { collection, getDocs, addDoc, doc, updateDoc, deleteDoc } from "firebase/firestore"
import { db } from "../services/firebase"

const COLLECTION = "planos_empresariais"

type Plano = {
  id: string
  nome: string
  valor: number
  descricao: string
  ativo: boolean
}

type FormData = {
  nome: string
  valor: string
  descricao: string
  ativo: boolean
}

const formInicial: FormData = {
  nome: "",
  valor: "",
  descricao: "",
  ativo: true,
}

function formatar(valor: number) {
  return valor.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  })
}

export default function PlanosEmpresariais() {

  const [planos, setPlanos] = useState<Plano[]>([])
  const [loading, setLoading] = useState(true)
  const [erro, setErro] = useState("")
  const [busca, setBusca] = useState("")

  const [modal, setModal] = useState(false)
  const [modo, setModo] = useState<"novo" | "editar">("novo")
  const [editId, setEditId] = useState<string | null>(null)
  const [form, setForm] = useState<FormData>(formInicial)

  useEffect(() => {
    carregar()
  }, [])

  async function carregar() {
    try {
      const snapshot = await getDocs(collection(db, COLLECTION))

      const lista: Plano[] = []

      snapshot.forEach((docItem) => {
        lista.push({
          id: docItem.id,
          ...docItem.data()
        } as Plano)
      })

      setPlanos(lista)

    } catch (err) {
      console.error(err)
      setErro("Erro ao carregar planos")
    } finally {
      setLoading(false)
    }
  }

  function abrirNovo() {
    setModo("novo")
    setForm(formInicial)
    setModal(true)
  }

  function abrirEditar(plano: Plano) {
    setModo("editar")
    setEditId(plano.id)
    setForm({
      nome: plano.nome,
      valor: String(plano.valor),
      descricao: plano.descricao,
      ativo: plano.ativo,
    })
    setModal(true)
  }

  async function salvar(e: React.FormEvent) {
    e.preventDefault()

    const payload = {
      nome: form.nome,
      valor: Number(form.valor.replace(",", ".")),
      descricao: form.descricao,
      ativo: form.ativo,
    }

    try {

      if (modo === "novo") {

        const docRef = await addDoc(collection(db, COLLECTION), payload)

        setPlanos((prev) => [
          { id: docRef.id, ...payload },
          ...prev
        ])

      } else if (editId) {

        await updateDoc(doc(db, COLLECTION, editId), payload)

        setPlanos((prev) =>
          prev.map((p) =>
            p.id === editId ? { id: p.id, ...payload } : p
          )
        )

      }

      setModal(false)

    } catch (err) {
      console.error(err)
      alert("Erro ao salvar plano")
    }
  }

  async function remover(id: string) {
    if (!confirm("Remover plano?")) return

    try {

      await deleteDoc(doc(db, COLLECTION, id))

      setPlanos((prev) => prev.filter((p) => p.id !== id))

    } catch (err) {
      console.error(err)
      alert("Erro ao remover plano")
    }
  }

  async function toggle(plano: Plano) {

    const novoStatus = !plano.ativo

    try {

      await updateDoc(doc(db, COLLECTION, plano.id), {
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

  const filtrados = useMemo(() => {
    return planos.filter((p) =>
      p.nome.toLowerCase().includes(busca.toLowerCase())
    )
  }, [planos, busca])

  return (
    <div className="planos-page">

      <div className="planos-header">
        <div>
          <h1>Planos Empresariais</h1>
          <p className="planos-subtitle">
            Gerencie planos empresariais
          </p>
        </div>

        <button className="btn-adicionar" onClick={abrirNovo}>
          Novo Plano
        </button>
      </div>

      <div className="planos-toolbar">
        <input
          className="planos-busca"
          placeholder="Buscar plano..."
          value={busca}
          onChange={(e) => setBusca(e.target.value)}
        />
      </div>

      {erro && <div className="planos-alerta-erro">{erro}</div>}

      <div className="planos-table">

        {loading ? (
          <div className="planos-loading">Carregando...</div>
        ) : filtrados.length === 0 ? (
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

              {filtrados.map((plano) => (

                <tr key={plano.id}>
                  <td>{plano.nome}</td>
                  <td>{plano.descricao}</td>
                  <td>{formatar(plano.valor)}</td>

                  <td>
                    <span className={plano.ativo ? "status-ativo" : "status-inativo"}>
                      {plano.ativo ? "Ativo" : "Inativo"}
                    </span>
                  </td>

                  <td>
                    <div className="plano-acoes">

                      <button className="btn-editar" onClick={() => abrirEditar(plano)}>
                        Editar
                      </button>

                      <button className="btn-status" onClick={() => toggle(plano)}>
                        {plano.ativo ? "Desativar" : "Ativar"}
                      </button>

                      <button className="btn-remover" onClick={() => remover(plano.id)}>
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

      {modal && (
        <div className="modal-overlay">

          <div className="modal-plano">

            <h2>{modo === "novo" ? "Novo Plano" : "Editar Plano"}</h2>

            <form onSubmit={salvar} className="modal-form">

              <input
                placeholder="Nome"
                value={form.nome}
                onChange={(e) => setForm({ ...form, nome: e.target.value })}
              />

              <input
                placeholder="Valor"
                value={form.valor}
                onChange={(e) => setForm({ ...form, valor: e.target.value })}
              />

              <textarea
                placeholder="Descrição"
                value={form.descricao}
                onChange={(e) => setForm({ ...form, descricao: e.target.value })}
              />

              <label>
                <input
                  type="checkbox"
                  checked={form.ativo}
                  onChange={(e) => setForm({ ...form, ativo: e.target.checked })}
                />
                Ativo
              </label>

              <div className="modal-acoes">
                <button type="button" onClick={() => setModal(false)}>
                  Cancelar
                </button>

                <button type="submit">
                  Salvar
                </button>
              </div>

            </form>

          </div>

        </div>
      )}

    </div>
  )
}