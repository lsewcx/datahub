import axios from '@/request/axios'

export const getProjects = () => {
    return axios.get('/api/projects')
}