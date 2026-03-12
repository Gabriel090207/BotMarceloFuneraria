import "../styles/urnas.css"

export default function Urnas(){

  const urnas = [

    {
      id:1,
      nome:"Urna Simples",
      tipo:"Simples",
      preco:"R$ 800"
    },

    {
      id:2,
      nome:"Urna Intermediária",
      tipo:"Intermediária",
      preco:"R$ 1.200"
    },

    {
      id:3,
      nome:"Urna Premium",
      tipo:"Premium",
      preco:"R$ 2.000"
    }

  ]

  return(

    <div className="urnas-page">

      <div className="urnas-header">

        <h1>Urnas</h1>

        <button className="btn-adicionar">
          + Nova Urna
        </button>

      </div>

      <div className="urnas-table">

        <table>

          <thead>

            <tr>

              <th>Nome</th>
              <th>Tipo</th>
              <th>Preço</th>
              <th>Ações</th>

            </tr>

          </thead>

          <tbody>

            {urnas.map((urna)=>(

              <tr key={urna.id}>

                <td>{urna.nome}</td>

                <td>{urna.tipo}</td>

                <td>{urna.preco}</td>

                <td>

                  <div className="urna-acoes">

                    <button className="btn-editar">
                      Editar
                    </button>

                    <button className="btn-remover">
                      Remover
                    </button>

                  </div>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>

  )

}