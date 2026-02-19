import { useEffect } from 'react'
import { useConfigStore } from '@/stores/configStore'

export function useParams() {
  const { schema, fetchSchema, loading } = useConfigStore()

  useEffect(() => {
    if (!schema && !loading) {
      fetchSchema()
    }
  }, [schema, loading, fetchSchema])

  return { schema, loading }
}
