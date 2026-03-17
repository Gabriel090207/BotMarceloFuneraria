import { Navigate } from "react-router-dom"
import { useEffect, useState } from "react"
import { onAuthStateChanged } from "firebase/auth"
import { auth } from "../services/firebase"

export default function ProtectedRoute({children}:any){

  const [user,setUser] = useState<any>(null)
  const [loading,setLoading] = useState(true)

  useEffect(()=>{

    const unsub = onAuthStateChanged(auth,(u)=>{

      setUser(u)
      setLoading(false)

    })

    return ()=>unsub()

  },[])

  if(loading){

    return <p>Carregando...</p>

  }

  if(!user){

    return <Navigate to="/login"/>

  }

  return children

}