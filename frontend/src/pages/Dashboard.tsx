import "../styles/dashboard.css"
import { useEffect, useState } from "react"
import { collection, getDocs, query, where} from "firebase/firestore"
import { db } from "../services/firebase"

export default function Dashboard(){

const [pedidos, setPedidos] = useState<any[]>([])

useEffect(() => {

  async function carregarPedidos(){

  
  const q = query(
  collection(db,"pedidos"),
  where("tipo","in",["funeraria","plano"])
)
const snapshot = await getDocs(q)

    const lista:any[] = []

    snapshot.forEach((doc)=>{

      lista.push({
        id:doc.id,
        ...doc.data()
      })

    })

    setPedidos(lista)

  }

  carregarPedidos()

},[])

function renderStatus(status:string){

  if(status === "aberto"){
    return <span className="status status-open">Em Aberto </span>
  }

  if(status === "pago"){
    return <span className="status status-paid">Pago</span>
  }

  if(status === "cancelado"){
    return <span className="status status-cancelado">Cancelado</span>
  }

  return <span>{status}</span>
}

return(

<div className="dashboard">

<h1>Dashboard</h1>

<div className="cards">

<div className="card">
<div className="card-title">Pedidos hoje</div>
<div className="card-value">{pedidos.length}</div>
</div>

<div className="card">
<div className="card-title">Pedidos no mês</div>
<div className="card-value">{pedidos.length}</div>
</div>

<div className="card">
<div className="card-title">Sepultamentos</div>
<div className="card-value">0</div>
</div>

<div className="card">
<div className="card-title">Cremações</div>
<div className="card-value">0</div>
</div>

</div>

<div className="pedidos">

<h2>Últimos pedidos</h2>

<table>

<thead>

<tr>
<th>Cliente</th>
<th>Telefone</th>
<th>Serviço</th>
<th>Status</th>
</tr>

</thead>

<tbody>

{pedidos.map((pedido)=>(

<tr key={pedido.id}>

<td>{pedido.nome}</td>

<td>{pedido.telefone || "-"}</td>

<td>{pedido.tipo}</td>

<td>{renderStatus(pedido.status)}</td>

</tr>

))}

</tbody>

</table>

</div>

</div>

)

}