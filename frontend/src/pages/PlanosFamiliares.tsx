import "../styles/planos.css"

export default function PlanosFamiliares(){

  const planos = [

    {
      id:1,
      nome:"Plano Essencial",
      valor:"R$ 39,90"
    },

    {
      id:2,
      nome:"Plano Completo",
      valor:"R$ 69,90"
    }

  ]

  return(

    <div className="planos-page">

      <div className="planos-header">

        <h1>Planos Familiares</h1>

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