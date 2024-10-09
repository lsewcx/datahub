export default [
  {
    url: '/api/projects',
    method: 'get',
    response: () => {
      return {
        code: 200,
        data: [
          {
            id: '1',
            name: '项目1',
            date: '2021-09-01',
            message: 'success',
            totals: 100,
            badge: "目标检测"
          },
          {
            id: '2',
            name: '项目2',
            date: '2021-09-02',
            message: 'success',
            totals: 200,
            badge: "图像分类"
          },
          {
            id: '3',
            name: '项目3',
            date: '2021-09-03',
            message: 'success',
            totals: 300,
            badge: "图像分割"
          },
          {
            id: '4',
            name: '项目4',
            date: '2021-09-04',
            message: 'success',
            totals: 400,
            badge: "图像检测"
          },
          {
            id: '5',
            name: '项目5',
            date: '2021-09-05',
            message: 'success',
            totals: 500,
            badge: "图像分类"
          },
          {
            id: '6',
            name: '项目6',
            date: '2021-09-06',
            message: 'success',
            totals: 600,
            badge: "图像分割"
          },
          {
            id: '7',
            name: '项目7',
            date: '2021-09-07',
            message: 'success',
            totals: 700,
            badge: "目标检测"
          },
          {
            id: '8',
            name: '项目8',
            date: '2021-09-08',
            message: 'success',
            totals: 800,
            badge: "图像检测"
          },
          {
            id: '9',
            name: '项目9',
            date: '2021-09-09',
            message: 'success',
            totals: 900,
            badge: "图像分类"
          },
          {
            id: '10',
            name: '项目10',
            date: '2021-09-10',
            message: 'success',
            totals: 1000,
            badge: "图像分割"
          },
        ],
      }
    },
  },
  {
    url: '/api/projects/delete',
    method : 'post',
    response: () => {
      return {
        code: 200,
        message: '删除成功'
      }
    }
  }
]