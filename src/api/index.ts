import axios from '@/request/axios'

export const getProjects = () => {
    return axios.get('/api/projects')
}

export const delProject = (id: string) => {
    return axios.post('/api/projects/delete', { id } )
}