import { useState } from "react"
import { signInWithEmailAndPassword } from "firebase/auth"
import { auth } from "../services/firebase"

import { useNavigate } from "react-router-dom"

import { FiLock, FiMail } from "react-icons/fi"

import "../styles/login.css"

export default function Login(){

  const navigate = useNavigate()

  const [email,setEmail] = useState("")
  const [senha,setSenha] = useState("")

  const [loading,setLoading] = useState(false)

  const [erroEmail,setErroEmail] = useState("")
  const [erroSenha,setErroSenha] = useState("")
  const [erroGeral,setErroGeral] = useState("")

  async function logar(){

    setErroEmail("")
    setErroSenha("")
    setErroGeral("")

    if(!email){
      setErroEmail("Informe o email")
      return
    }

    if(!senha){
      setErroSenha("Informe a senha")
      return
    }

    try{

      setLoading(true)

      await signInWithEmailAndPassword(auth,email,senha)

      navigate("/")

    }catch(e:any){

      const code = e.code

      if(code === "auth/user-not-found"){

        setErroEmail("Email não encontrado")

      }

      else if(code === "auth/wrong-password"){

        setErroSenha("Senha incorreta")

      }

      else if(code === "auth/invalid-email"){

        setErroEmail("Email inválido")

      }

      else{

        setErroGeral("Email ou senha incorretos")

      }

    }finally{

      setLoading(false)

    }

  }

  return(

    <div className="login-page">

      <div className="login-card">

        <img
          src="/logo.png"
          className="login-logo"
        />

        <h1>Painel Administrativo</h1>

        <div className="login-form">

          <div className={`login-input ${erroEmail ? "input-error" : ""}`}>

            <FiMail/>

            <input
              placeholder="Email"
              value={email}
              onChange={(e)=>setEmail(e.target.value)}
            />

          </div>

          {erroEmail && <span className="login-error">{erroEmail}</span>}

          <div className={`login-input ${erroSenha ? "input-error" : ""}`}>

            <FiLock/>

            <input
              type="password"
              placeholder="Senha"
              value={senha}
              onChange={(e)=>setSenha(e.target.value)}
            />

          </div>

          {erroSenha && <span className="login-error">{erroSenha}</span>}

          {erroGeral && <span className="login-error">{erroGeral}</span>}

          <button
            onClick={logar}
            disabled={loading}
            className="login-button"
          >

            {loading ? "Entrando..." : "Entrar"}

          </button>

        </div>

      </div>

    </div>

  )

}