<template>
  <div class="news-detail">
    <van-nav-bar
      title="新闻详情"
      left-text="返回"
      left-arrow
      @click-left="onClickLeft"
      fixed
    />
    
    <div class="detail-content" v-if="newsStore.newsDetail.id && !loading">
      <div class="title-container">
        <h1 class="title">{{ newsStore.newsDetail.title }}</h1>
        <van-button
          class="favorite-btn"
          :icon="isFavorite ? 'star' : 'star-o'"
          :class="{ 'is-favorite': isFavorite }"
          @click="toggleFavorite"
        />
      </div>

      <div class="info">
        <span>{{ newsStore.newsDetail.author }}</span>
        <span>{{ newsStore.newsDetail.publishTime }}</span>
        <span>{{ newsStore.newsDetail.views }} 阅读</span>
      </div>

      <div class="cover" v-if="newsStore.newsDetail.image">
        <img :src="newsStore.newsDetail.image" :alt="newsStore.newsDetail.title">
      </div>

      <div class="content">
        <p v-for="(paragraph, index) in contentParagraphs" :key="index">
          {{ paragraph }}
        </p>
      </div>

      <div class="related-news" v-if="newsStore.newsDetail.relatedNews?.length">
        <h3>相关推荐</h3>
        <div class="related-list">
          <div
            class="related-item"
            v-for="item in newsStore.newsDetail.relatedNews"
            :key="item.id"
            @click="goToRelatedNews(item.id)"
          >
            <div class="related-image">
              <img :src="item.image" :alt="item.title">
            </div>
            <div class="related-info">
              <div class="related-title">{{ item.title }}</div>
              <div class="related-meta">{{ item.author }} · {{ item.views }} 阅读</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <van-loading v-else-if="loading" class="loading-center" />
    <van-empty v-else description="新闻不存在" />
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNewsStore } from '../store/modules/news'
import { useHistoryStore } from '../store/modules/history'
import { useFavoriteStore } from '../store/modules/favorite'
import { useUserStore } from '../store/user'
import { showToast } from 'vant'

const route = useRoute()
const router = useRouter()
const newsStore = useNewsStore()
const historyStore = useHistoryStore()
const favoriteStore = useFavoriteStore()
const userStore = useUserStore()

// 加载中状态
const loading = ref(false)

// 获取路由参数中的新闻ID
const newsId = computed(() => Number(route.params.id))

// 将内容拆分为段落
const contentParagraphs = computed(() => {
  if (!newsStore.newsDetail.content) return []
  return newsStore.newsDetail.content.split('\n\n').filter(p => p.trim())
})

// 返回上一页
const onClickLeft = () => {
  router.back()
}

// 跳转到相关新闻
const goToRelatedNews = (id) => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
  router.push(`/news/detail/${id}`)
}

// 加载新闻详情（抽取为独立函数，供 onMounted 和 watch 复用）
const loadNewsDetail = async () => {
  loading.value = true
  await newsStore.getNewsDetail(newsId.value)

  if (newsStore.newsDetail.id) {
    // 记录浏览历史
    if (userStore.getLoginStatus) {
      try {
        await historyStore.addHistoryApi(newsStore.newsDetail.id)
      } catch (error) {
        console.error('记录浏览历史失败:', error)
      }
    }

    // 加载收藏数据
    favoriteStore.loadFavorites()

    // 检查文章收藏状态
    if (userStore.getLoginStatus) {
      const result = await favoriteStore.checkFavoriteStatusApi(newsStore.newsDetail.id)
      if (result.success && !result.isLocal) {
        if (result.isFavorite && !favoriteStore.isFavorite(newsStore.newsDetail.id)) {
          favoriteStore.addFavorite(newsStore.newsDetail)
        } else if (!result.isFavorite && favoriteStore.isFavorite(newsStore.newsDetail.id)) {
          favoriteStore.removeFavorite(newsStore.newsDetail.id)
        }
      }
    }
  }
  loading.value = false
}

// 监听路由参数变化（从相关推荐跳转时复用同一组件）
watch(
  () => route.params.id,
  async (newId) => {
    if (newId) {
      await loadNewsDetail()
    }
  }
)

// 判断当前新闻是否已收藏
const isFavorite = computed(() => {
  return favoriteStore.isFavorite(newsId.value)
})

// 切换收藏状态
const toggleFavorite = async () => {
  // 判断用户是否已登录
  if (!userStore.getLoginStatus) {
    // 未登录则跳转到登录页
    showToast({
      message: '请先登录后再收藏',
      position: 'bottom',
    })
    router.push('/login')
    return
  }
  
  // 已登录则调用API切换收藏状态
  const status = await favoriteStore.toggleFavorite(newsStore.newsDetail)
  
  if (status === true) {
    showToast({
      message: '已添加到收藏',
      position: 'bottom',
    })
  } else if (status === false) {
    showToast({
      message: '已取消收藏',
      position: 'bottom',
    })
  } else {
    // status为null表示操作失败
    showToast({
      message: '操作失败，请稍后重试',
      position: 'bottom',
    })
  }
}

// 组件挂载时加载新闻详情
onMounted(async () => {
  await loadNewsDetail()
})
</script>

<style scoped>
.news-detail {
  padding-top: 46px;
  background-color: #fff;
  min-height: 100vh;
}

.detail-content {
  padding: 16px;
}

.title-container {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 12px;
}

.title {
  font-size: 22px;
  font-weight: bold;
  line-height: 1.4;
  margin: 0;
  flex: 1;
}

.favorite-btn {
  flex-shrink: 0;
  margin-left: 10px;
  padding: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
}

.favorite-btn.is-favorite {
  color: #ff9500;
}

.info {
  display: flex;
  font-size: 12px;
  color: #999;
  margin-bottom: 16px;
}

.info span {
  margin-right: 12px;
}

.cover {
  margin-bottom: 16px;
}

.cover img {
  width: 100%;
  border-radius: 4px;
}

.content {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
}

.content p {
  margin-bottom: 16px;
  text-align: justify;
}

.loading-center {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.related-news {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 8px solid #f5f5f5;
}

.related-news h3 {
  font-size: 18px;
  margin: 0 0 16px;
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.related-item {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 4px 0;
}

.related-item:active {
  background-color: #f5f5f5;
}

.related-image {
  width: 100px;
  height: 70px;
  margin-right: 12px;
  flex-shrink: 0;
  border-radius: 4px;
  overflow: hidden;
  background-color: #f0f0f0;
}

.related-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.related-info {
  flex: 1;
  min-width: 0;
}

.related-title {
  font-size: 14px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.related-meta {
  font-size: 12px;
  color: #999;
  margin-top: 6px;
}
</style>