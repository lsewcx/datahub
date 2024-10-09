import axios from '@/request/axios'

export const getProjects = (page: number) => {
    return axios.get('/api/projects', {
        params: {
            page: page
        }
    })
}

export const delProject = (id: string) => {
    return axios.post('/api/projects/delete', { id } )
}