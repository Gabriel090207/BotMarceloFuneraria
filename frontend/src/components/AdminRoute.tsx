import { useEffect, useState } from "react"
import type { ReactNode } from "react"
import { onAuthStateChanged } from "firebase/auth"
import { doc, getDoc } from "firebase/firestore"
import { Navigate } from "react-router-dom"
import { auth, db } from "../services/firebase"

export default function AdminRoute({ children }: { children: ReactNode }) {
  const [estado, setEstado] = useState("carregando")
  useEffect(() => {
    let versao = 0
    const cancelar = onAuthStateChanged(auth, async usuario => {
      const atual = ++versao
      setEstado("carregando")
      if (!usuario) {
        setEstado("login")
        return
      }
      try {
        const perfil = await getDoc(doc(db, "users", usuario.uid))
        if (atual !== versao) return
        setEstado(perfil.exists() && perfil.data().role === "admin" ? "admin" : "negado")
      } catch {
        if (atual === versao) setEstado("erro")
      }
    })
    return () => { versao++; cancelar() }
  }, [])

  if (estado === "carregando") return <p role="status">Verificando acesso...</p>
  if (estado === "login") return <Navigate to="/login" replace />
  if (estado === "erro") return <p role="alert">Não foi possível verificar seu acesso. Recarregue a página para tentar novamente.</p>
  if (estado !== "admin") return <p role="alert">Esta página está disponível somente para administradores.</p>
  return children
}
