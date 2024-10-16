<template>
    <div>
        <Button class="mt-10 ml-14" @click="openCreateProjectDialog">创建新项目</Button>
        <div class="flex flex-wrap mt-1 ml-10">
            <div v-for="item in data" :key="item.id" class="m-4">
                <Card class="w-[600px]">
                    <CardHeader>
                        <CardTitle>{{ item.name }}
                            <DropdownMenu>
                                <DropdownMenuTrigger as-child>
                                    <Button variant="outline" class="p-2 ml-96">
                                        <MoreHorizontal class="h-4 w-4" />
                                    </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent class="w-56">
                                    <DropdownMenuItem @click="confirmDelete(item.id)">
                                        <Trash class="mr-2 h-4 w-4" />
                                        <span>删除项目</span>
                                    </DropdownMenuItem>
                                </DropdownMenuContent>
                            </DropdownMenu>
                        </CardTitle>
                        <CardDescription>{{ item.date }} </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Badge>{{ item.badge }}</Badge>
                        <p>images {{ item.totals }}</p>
                    </CardContent>
                </Card>
            </div>
        </div>
        <div class="flex justify-center mt-4">
            <Pagination v-slot="{ page }" :total="totalPages" :sibling-count="1" show-edges :default-page="1" @update:page="handlePageChange">
                <PaginationList v-slot="{ items }" class="flex items-center gap-1">
                    <PaginationFirst />
                    <PaginationPrev />
                    <template v-for="(item, index) in items">
                        <PaginationListItem v-if="item.type === 'page'" :key="index" :value="item.value" as-child>
                            <Button class="w-10 h-10 p-0" :variant="item.value === page ? 'default' : 'outline'">
                                {{ item.value }}
                            </Button>
                        </PaginationListItem>
                        <PaginationEllipsis v-else :key="item.type" :index="index" />
                    </template>
                    <PaginationNext />
                    <PaginationLast />
                </PaginationList>
            </Pagination>
        </div>
        <Dialog v-model:open="showDialog">
            <DialogContent class="sm:max-w-md">
                <DialogHeader>
                    <DialogTitle>确认删除</DialogTitle>
                    <DialogDescription>
                        你确定要删除这个项目吗？
                    </DialogDescription>
                </DialogHeader>
                <DialogFooter class="sm:justify-start">
                    <Button type="button" variant="default" @click="deleteProject">
                        确认
                    </Button>
                    <Button type="button" variant="secondary" @click="closeDialog">
                        取消
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
        <Dialog v-model:open="showCreateProjectDialog">
            <DialogContent class="sm:max-w-md">
                <DialogHeader>
                    <DialogTitle>创建新项目</DialogTitle>
                    <DialogDescription>
                        请填写以下信息以创建新项目。
                    </DialogDescription>
                </DialogHeader>
                <form @submit.prevent="createNewProject">
                    <div class="mb-4">
                        <label for="name" class="block text-sm font-medium text-gray-700">项目名称</label>
                        <input v-model="newProject.name" type="text" id="name" class="mt-1 block w-full" required />
                    </div>
                    <div class="mb-4">
                        <label for="description" class="block text-sm font-medium text-gray-700">项目描述</label>
                        <input v-model="newProject.description" type="text" id="description" class="mt-1 block w-full" required />
                    </div>
                    <div class="mb-4">
                        <label for="badge" class="block text-sm font-medium text-gray-700">项目徽章</label>
                        <input v-model="newProject.badge" type="text" id="badge" class="mt-1 block w-full" required />
                    </div>
                    <div class="mb-4">
                        <label for="file" class="block text-sm font-medium text-gray-700">项目文件</label>
                        <input @change="handleFileChange" type="file" class="mt-1 block w-full" required />
                    </div>
                    <DialogFooter class="sm:justify-start">
                        <Button type="submit" variant="default">
                            创建
                        </Button>
                        <Button type="button" variant="secondary" @click="closeCreateProjectDialog">
                            取消
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getProjects, delProject} from '@/api/index'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import moment from 'moment'
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'
import {
    MoreHorizontal,
    Trash,
} from 'lucide-vue-next'
import {
    DropdownMenu,
    DropdownMenuTrigger,
    DropdownMenuContent,
    DropdownMenuItem,
} from '@/components/ui/dropdown-menu'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog'
import {
    Pagination,
    PaginationEllipsis,
    PaginationFirst,
    PaginationLast,
    PaginationList,
    PaginationListItem,
    PaginationNext,
    PaginationPrev,
} from '@/components/ui/pagination'
import { project } from '../types/index'
import axios from 'axios'

const data = ref<project[]>([])
const showDialog = ref(false)
const showCreateProjectDialog = ref(false)
const projectIdToDelete = ref<string | null>(null)
const totalPages = ref(0)

const newProject = ref({
    name: '',
    description: '',
    badge: '',
    date: '',
    file: null as File | null
})

const confirmDelete = (id: string) => {
    projectIdToDelete.value = id
    showDialog.value = true
}

const closeDialog = () => {
    showDialog.value = false
    projectIdToDelete.value = null
}

const openCreateProjectDialog = () => {
    showCreateProjectDialog.value = true
}

const closeCreateProjectDialog = () => {
    showCreateProjectDialog.value = false
}

const handleFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement
    if (target.files && target.files.length > 0) {
        newProject.value.file = target.files[0]
    }
}

const createNewProject = async () => {
    try {
        const formData = new FormData()
        formData.append('name', newProject.value.name)
        formData.append('description', newProject.value.description)
        formData.append('badge', newProject.value.badge)
        formData.append('date', moment().format('YYYY-MM-DD HH:mm:ss'))
        if (newProject.value.file) {
            formData.append('file', newProject.value.file)
        }
        await axios.post('/api/projects/create', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then((res) => {
            console.log(res)
        })
        closeCreateProjectDialog()
        fetchProjects(1) // 重新加载项目列表
    } catch (error) {
        console.error('创建项目失败:', error)
    }
}

const deleteProject = async () => {
    if (projectIdToDelete.value !== null) {
        await delProject(projectIdToDelete.value)
        data.value = data.value.filter(item => item.id !== projectIdToDelete.value) //从数组中删除
        closeDialog()
    }
}

const fetchProjects = async (page: number) => {
    const res = await getProjects(page)
    console.log(res)
    data.value = res.data
    totalPages.value = res.totalPage
}

const handlePageChange = (page: number) => {
    fetchProjects(page)
}

onMounted(() => {
    fetchProjects(1)
})
</script>