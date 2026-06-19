import type { ContactPayload, ContactResponse, ErrorBody } from '@/types'

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''

export class ApiError extends Error {
	readonly status: number

	constructor(message: string, status: number) {
		super(message)
		this.name = 'ApiError'
		this.status = status
	}
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
	let response: Response
	try {
		const { headers, ...rest } = init ?? {}
		response = await fetch(`${BASE_URL}${path}`, {
			headers: { 'Content-Type': 'application/json', ...headers },
			...rest,
		})
	} catch {
		throw new ApiError('Сеть недоступна. Проверьте подключение.', 0)
	}

	if (!response.ok) {
		let detail = `Ошибка сервера (${response.status})`
		try {
			const body = (await response.json()) as ErrorBody
			if (body.detail) detail = body.detail
		} catch {
			/* response had no JSON body */
		}
		throw new ApiError(detail, response.status)
	}

	return (await response.json()) as T
}

export function submitContact(
	payload: ContactPayload,
): Promise<ContactResponse> {
	return request<ContactResponse>('/api/contact', {
		method: 'POST',
		// Marker so the backend rate-limits only genuine form submissions.
		headers: { 'X-Contact-Source': 'web-form' },
		body: JSON.stringify(payload),
	})
}
