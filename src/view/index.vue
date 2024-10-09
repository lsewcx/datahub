<template>
    <div>
        <Button class="mt-10 ml-14">创建新项目</Button>
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
                        <CardDescription>{{ item.date }}</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Badge>{{ item.badge }}</Badge>
                        <p>images {{ item.totals }}</p>
                    </CardContent>
                </Card>
            </div>
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
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getProjects, delProject } from '@/api/index'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
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
    DialogTrigger
} from '@/components/ui/dialog'
import { project } from '../types/index'

const data = ref<project[]>([])
const showDialog = ref(false)
const projectIdToDelete = ref<string | null>(null)

const confirmDelete = (id: string) => {
    projectIdToDelete.value = id
    showDialog.value = true
}

const closeDialog = () => {
    showDialog.value = false
    projectIdToDelete.value = null
}

const deleteProject = async () => {
    if (projectIdToDelete.value !== null) {
        await delProject(projectIdToDelete.value)
        data.value = data.value.filter(item => item.id !== projectIdToDelete.value) //从数组中删除
        closeDialog()
    }
}

onMounted(() => {
    getProjects().then((res) => {
        data.value = res.data
    })
})
</script>