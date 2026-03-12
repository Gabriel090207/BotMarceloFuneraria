import "../styles/planos.css"

export default function PlanosEmpresariais(){

  const planos = [

    {
      id:1,
      nome:"Plano Empresa Básico",
      valor:"R$ 199,90"
    },

    {
      id:2,
      nome:"Plano Empresa Premium",
      valor:"R$ 399,90"
    }

  ]

  return(

    <div className="planos-page">

      <div className="planos-header">

        <h1>Planos Empresariais</h1>

        <button className="btn-adicionar">
          Novo Plano
        </button>

      </div>

      <div className="planos-table">

        <table>

          <thead>

            <tr>
              <th>Plano</th>
              <th>Valor Mensal</th>
              <th>Ações</th>
            </tr>

          </thead>

          <tbody>

            {planos.map((plano)=>(

              <tr key={plano.id}>

                <td>{plano.nome}</td>

                <td>{plano.valor}</td>

                <td>

                  <div className="plano-acoes">

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