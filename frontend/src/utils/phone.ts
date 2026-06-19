/**
 * Russian phone mask. Formats raw input into "+7 999 123-45-67" format.
 */
export function formatRuPhone(input: string): string {
	let digits = input.replace(/\D/g, '')
	if (!digits) return ''

	if (digits.startsWith('8') || digits.startsWith('7')) {
		digits = digits.slice(1)
	}
	digits = digits.slice(0, 10)

	const a = digits.slice(0, 3)
	const b = digits.slice(3, 6)
	const c = digits.slice(6, 8)
	const d = digits.slice(8, 10)

	let out = '+7'
	if (a) out += ` ${a}`
	if (b) out += ` ${b}`
	if (c) out += ` ${c}`
	if (d) out += `-${d}`
	return out
}
