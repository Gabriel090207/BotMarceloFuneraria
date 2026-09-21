import { collection, deleteDoc, doc, getDocs, runTransaction, serverTimestamp, updateDoc } from "firebase/firestore"
import { db } from "./firebase"
import { normalizarTelefoneBrasileiro } from "../utils/telefoneBrasileiro"

export interface NumeroInterno {
  id: string
  nome: string
  telefone: string
  telefone_normalizado: string
  ativo: boolean
}

export class CadastroNumeroError extends Error {}

const colecao = "numeros_internos"

export async function listarNumerosInternos(): Promise<NumeroInterno[]> {
  const snapshot = await getDocs(collection(db, colecao))
  return snapshot.docs.map(documento => {
    const dados = documento.data()
    return {
      id: documento.id,
      nome: typeof dados.nome === "string" ? dados.nome : "Sem nome",
      telefone: typeof dados.telefone === "string" ? dados.telefone : documento.id,
      telefone_normalizado: documento.id,
      ativo: dados.ativo === true,
    }
  }).sort((a, b) => a.nome.localeCompare(b.nome, "pt-BR"))
}

export async function cadastrarNumeroInterno(nome: string, telefone: string): Promise<void> {
  const nomeLimpo = nome.trim()
  const normalizado = normalizarTelefoneBrasileiro(telefone)
  if (!normalizado) throw new CadastroNumeroError("Informe um telefone brasileiro válido, com DDD.")
  const ref = doc(db, colecao, normalizado)
  const nacional = normalizado.slice(2)
  const telefoneExibicao = `+55 (${nacional.slice(0, 2)}) ${nacional.slice(2, -4)}-${nacional.slice(-4)}`
  await runTransaction(db, async transacao => {
    const existente = await transacao.get(ref)
    if (existente.exists()) throw new CadastroNumeroError("Este telefone já está cadastrado. Consulte a lista abaixo.")
    transacao.set(ref, {
      nome: nomeLimpo,
      telefone: telefoneExibicao,
      telefone_normalizado: normalizado,
      ativo: true,
      criado_em: serverTimestamp(),
      atualizado_em: serverTimestamp(),
    })
  })
}

export async function definirStatusNumeroInterno(id: string, ativo: boolean): Promise<void> {
  await updateDoc(doc(db, colecao, id), { ativo, atualizado_em: serverTimestamp() })
}

export async function excluirNumeroInterno(id: string): Promise<void> {
  await deleteDoc(doc(db, colecao, id))
}
