import { useState } from "react"

import { useEffect } from "react"
import { collection, getDocs } from "firebase/firestore"
import { FiEdit } from "react-icons/fi"

import { createUserWithEmailAndPassword } from "firebase/auth"
import { auth, db } from "../../services/firebase"
import { doc, setDoc } from "firebase/firestore"

import { FiCheck } from "react-icons/fi"

import { updateDoc } from "firebase/firestore"

import "../../styles/usuarios.css"

export default function Usuarios(){

  const [nome,setNome] = useState("")
  const [sobrenome,setSobrenome] = useState("")
  const [email,setEmail] = useState("")
  const [senha,setSenha] = useState("")
  const [role,setRole] = useState("funcionario")


  const [loading,setLoading] = useState(false)

  const [sucesso,setSucesso] = useState(false)
const [mensagemSucesso,setMensagemSucesso] = useState("")

const [usuarios,setUsuarios] = useState<any[]>([])


const [editar,setEditar] = useState(false)
const [usuarioEdit,setUsuarioEdit] = useState<any>(null)


async function criarUsuario(){

  try{

    setLoading(true)

    const userAdmin = auth.currentUser

    if(!userAdmin) return

    const cred = await createUserWithEmailAndPassword(
      auth,
      email,
      senha
    )

    const uid = cred.user.uid

    await setDoc(doc(db,"users",uid),{

      nome,
      sobrenome,
      email,
      role,
      criado_em: new Date()

    })

    // voltar admin logado
    await auth.updateCurrentUser(userAdmin)

    setNome("")
    setSobrenome("")
    setEmail("")
    setSenha("")
    setRole("funcionario")

    carregarUsuarios()

   setMensagemSucesso("Usuário criado com sucesso")
setSucesso(true)

  }catch(e){

    console.error(e)

    alert("Erro ao criar usuário")

  }finally{

    setLoading(false)

  }

}


async function carregarUsuarios(){

  const snap = await getDocs(collection(db,"users"))

  const lista:any[] = []

  snap.forEach((doc)=>{

    lista.push({
      id:doc.id,
      ...doc.data()
    })

  })

  setUsuarios(lista)

}

async function salvarEdicao(){

  try{

    setLoading(true)

    await updateDoc(doc(db,"users",usuarioEdit.id),{

      nome,
      sobrenome,
      email,
      role

    })

    carregarUsuarios()

   

    setEditar(false)


     setNome("")
setSobrenome("")
setEmail("")
setSenha("")
setRole("funcionario")

    setMensagemSucesso("Usuário atualizado com sucesso")
setSucesso(true)

  }catch(e){

    console.error(e)

    alert("Erro ao editar usuário")

  }finally{

    setLoading(false)

  }

}

useEffect(()=>{

  carregarUsuarios()

},[])
  


  return(

  <div className="usuarios-page">

    <div className="usuarios-card">

      <h2>Criar usuário</h2>

      <div className="usuarios-grid">

        <div className="usuarios-field">

          <label>Nome</label>

          <input
            value={nome}
            onChange={(e)=>setNome(e.target.value)}
          />

        </div>

        <div className="usuarios-field">

          <label>Sobrenome</label>

          <input
            value={sobrenome}
            onChange={(e)=>setSobrenome(e.target.value)}
          />

        </div>

        <div className="usuarios-field">

          <label>Email</label>

          <input
            value={email}
            onChange={(e)=>setEmail(e.target.value)}
          />

        </div>

        <div className="usuarios-field">

          <label>Senha</label>

          <input
            type="password"
            value={senha}
            onChange={(e)=>setSenha(e.target.value)}
          />

        </div>

        <div className="usuarios-field">

          <label>Tipo de usuário</label>

          <select
            value={role}
            onChange={(e)=>setRole(e.target.value)}
          >

            <option value="admin">
              Administrador
            </option>

            <option value="funcionario">
              Funcionário
            </option>

          </select>

        </div>

      </div>

      <button
  className="btn-criar"
  onClick={criarUsuario}
  disabled={loading}
>


    

  {loading ? "Criando usuário..." : "Criar usuário"}

</button>

{sucesso && (

  <div className="modal-overlay">

    <div className="modal-sucesso">

      <FiCheck className="modal-icon"/>

     <h2>{mensagemSucesso}</h2>

      <button onClick={()=>setSucesso(false)}>
        OK
      </button>

    </div>

  </div>

)}

</div>


<div className="usuarios-table-card">

  <h2>Usuários cadastrados</h2>

  <table className="usuarios-table">

    <thead>

      <tr>
        <th>Nome</th>
        <th>Email</th>
        <th>Tipo</th>
        <th>Ações</th>
      </tr>

    </thead>

    <tbody>

      {usuarios.map((u:any)=>{

        return(

          <tr key={u.id}>

            <td>{u.nome} {u.sobrenome}</td>

            <td>{u.email}</td>

            <td>{u.role}</td>

            <td>

            <button
  className="btn-editar"
  onClick={()=>{

    setUsuarioEdit(u)

    setNome(u.nome)
    setSobrenome(u.sobrenome)
    setEmail(u.email)
    setRole(u.role)

    setEditar(true)

  }}
>
  <FiEdit/>
</button>

            </td>

          </tr>

        )

      })}

    </tbody>

  </table>

</div>


{editar && (

  <div className="modal-overlay">

    <div className="modal-editar">

      <h2>Editar usuário</h2>

      <div className="usuarios-grid">

        <div className="usuarios-field">

          <label>Nome</label>

          <input
            value={nome}
            onChange={(e)=>setNome(e.target.value)}
          />

        </div>

        <div className="usuarios-field">

          <label>Sobrenome</label>

          <input
            value={sobrenome}
            onChange={(e)=>setSobrenome(e.target.value)}
          />

        </div>

        <div className="usuarios-field">

          <label>Email</label>

          <input
            value={email}
            onChange={(e)=>setEmail(e.target.value)}
          />

        </div>

        <div className="usuarios-field">

          <label>Tipo</label>

          <select
            value={role}
            onChange={(e)=>setRole(e.target.value)}
          >

            <option value="admin">
              Administrador
            </option>

            <option value="funcionario">
              Funcionário
            </option>

          </select>

        </div>

      </div>

      <div className="editar-actions">

        <button
          className="btn-cancelar"
          onClick={()=>setEditar(false)}
        >
          Cancelar
        </button>

        <button
          className="btn-salvar"
          onClick={salvarEdicao}
          disabled={loading}
        >
          {loading ? "Salvando..." : "Salvar alterações"}
        </button>

      </div>

    </div>

  </div>

)}

    </div>


    

    

  )

}