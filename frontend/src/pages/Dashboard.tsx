import "../styles/dashboard.css"
import { useEffect, useState, useMemo } from "react"
import { collection, getDocs, query } from "firebase/firestore"
import { db } from "../services/firebase"

type Pedido = {
  id: string
  nome: string
  telefone?: string
  tipo: string
  status: string
  criado_em?: string
  dados?: any
}

export default function Dashboard(){

  const [pedidos, setPedidos] = useState<Pedido[]>([])
  const [loading, setLoading] = useState(true)
  const [erro, setErro] = useState("")

  useEffect(() => {

    async function carregarPedidos(){

      try{

        const q = query(collection(db,"pedidos"))

        const snapshot = await getDocs(q)

        const lista:Pedido[] = []

        snapshot.forEach((doc)=>{
          lista.push({
            id:doc.id,
            ...doc.data()
          } as Pedido)
        })

        setPedidos(lista)

      }catch(err){
        console.error(err)
        setErro("Erro ao carregar pedidos")
      }finally{
        setLoading(false)
      }

    }

    carregarPedidos()

  },[])

  // 🔥 FUNÇÃO QUE CONVERTE DATA CORRETAMENTE
 function dataLocal(dataString?: string){
  if(!dataString) return ""

  // 🔥 força tratar como UTC e converter para Brasil (-3h)
  const dataUTC = new Date(dataString)

  const dataBrasil = new Date(dataUTC.getTime() - (3 * 60 * 60 * 1000))

  return dataBrasil.toLocaleDateString("sv-SE")
}

  // 📅 HOJE
  const hoje = new Date().toLocaleDateString("sv-SE")

  const pedidosHoje = useMemo(() => {
    return pedidos.filter(p =>
      dataLocal(p.criado_em) === hoje
    )
  }, [pedidos])

  // 📅 MÊS
  const mesAtual = hoje.slice(0,7)

  const pedidosMes = useMemo(() => {
    return pedidos.filter(p =>
      dataLocal(p.criado_em).startsWith(mesAtual)
    )
  }, [pedidos])

  // ⚰️ SEPULTAMENTO
  const sepultamentos = useMemo(() => {
    return pedidos.filter(p => p.tipo === "sepultamento").length
  }, [pedidos])

  // 🔥 CREMAÇÃO
  const cremacao = useMemo(() => {
    return pedidos.filter(p => p.tipo === "cremacao").length
  }, [pedidos])

  function renderStatus(status:string){

    if(status === "novo" || status === "aberto"){
      return <span className="status status-open">Em Aberto</span>
    }

    if(status === "finalizado" || status === "pago"){
      return <span className="status status-paid">Finalizado</span>
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
          <div className="card-value">{pedidosHoje.length}</div>
        </div>

        <div className="card">
          <div className="card-title">Pedidos no mês</div>
          <div className="card-value">{pedidosMes.length}</div>
        </div>

        <div className="card">
          <div className="card-title">Sepultamentos</div>
          <div className="card-value">{sepultamentos}</div>
        </div>

        <div className="card">
          <div className="card-title">Cremações</div>
          <div className="card-value">{cremacao}</div>
        </div>

      </div>

      {erro && <div className="erro">{erro}</div>}

      <div className="pedidos">

        <h2>Últimos pedidos</h2>

        {loading ? (
          <div className="loading">Carregando...</div>
        ) : pedidos.length === 0 ? (
          <div className="vazio">Nenhum pedido encontrado</div>
        ) : (

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

              {pedidos.slice(0,10).map((pedido)=>(

                <tr key={pedido.id}>

                  <td>{pedido.nome}</td>

                  <td>{pedido.telefone || "-"}</td>

                  <td>
                    {pedido.tipo === "sepultamento" && "Sepultamento"}
                    {pedido.tipo === "cremacao" && "Cremação"}
                    {pedido.tipo === "translado" && "Translado"}
                    {!pedido.tipo && "Funerário"}
                  </td>

                  <td>{renderStatus(pedido.status)}</td>

                </tr>

              ))}

            </tbody>

          </table>

        )}

      </div>

    </div>

  )

}