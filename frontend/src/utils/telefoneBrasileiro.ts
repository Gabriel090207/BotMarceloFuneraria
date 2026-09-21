/** Mantém o mesmo contrato de core/numeros_internos.py, sem corrigir dígitos. */
export function normalizarTelefoneBrasileiro(numero: unknown): string | null {
  if (typeof numero !== "string") return null
  const texto = numero.replace(/^ +| +$/g, "")
  const formato = /^(?:\+?55 *)?(?:[0-9]{2}|\([0-9]{2}\)) *[0-9]{4,5}-?[0-9]{4}$/
  // Em JavaScript, $ também pode casar antes da última quebra de linha.
  if (formato.exec(texto)?.[0] !== texto) return null
  const digitos = texto.replace(/^\+/, "").replace(/[ ()-]/g, "")
  let nacional: string
  if (digitos.length === 12 || digitos.length === 13) {
    if (!digitos.startsWith("55")) return null
    nacional = digitos.slice(2)
  } else if ((digitos.length === 10 || digitos.length === 11) && !texto.startsWith("+")) {
    nacional = digitos
  } else {
    return null
  }
  if (!/^[1-9]{2}[2-9][0-9]{7,8}$/.test(nacional)) return null
  return "55" + nacional
}
