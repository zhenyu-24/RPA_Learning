import re
import time
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(channel="msedge", headless=False)
    context = browser.new_context(storage_state="bilibili")
    page = context.new_page()
    page.goto("https://www.bilibili.com/video/BV1zgCbBHE7Q/?vd_source=c52a6491548814d54a99f3b97b0df55c")

    # 等待页面加载
    page.wait_for_load_state("networkidle")

    print("=" * 60)
    print("开始收集推荐视频...")
    print("=" * 60)

    # 获取所有推荐视频项
    video_items = page.locator(
        "#mirror-vdcon > div.right-container > div > div.rcmd-tab > div.recommend-list-v1 > div.rec-list > div").all()
    url_list = []

    for i, item in enumerate(video_items):
        try:
            # 提取标题和BV号
            title_elem = item.locator(".info .title").first
            title = title_elem.text_content() if title_elem else "无标题"

            # 方法1: 通过查找 info > a 元素中的链接
            # info_link = item.locator("div > div.info > a").first
            # href = info_link.get_attribute("href") if info_link else "无链接
            # 方法2: 通过查找包含 /video/ 的链接
            all_links = item.locator('a[href^="/video/"]').first
            href = all_links.get_attribute("href") if all_links else "无链接"


            if href and '/video/' in href:
                # 构建完整URL
                full_url = f"https:{href}" if href.startswith("//") else f"https://www.bilibili.com{href}"

            print(f"视频 {len(url_list) + 1}:")
            print(f"  标题: {title.strip() if title else '无标题'}")
            print(f"  链接: {full_url}")
            print("-" * 40)

            url_list.append({
                'url': full_url,
                'title': title.strip() if title else '无标题',
            })

        except Exception as e:
            print(f"处理第 {i} 个项目时出错: {e}")
            continue

    print(f"\n总共收集到 {len(url_list)} 个推荐视频")

    # 等待当前视频播放结束
    print("\n" + "=" * 60)
    print("等待当前视频播放结束...")
    print("=" * 60)

    try:
        # 等待视频进入结束状态
        page.wait_for_function("""
            () => {
                const video = document.querySelector('video');
                return video && video.ended;
            }
        """, timeout=600000)  # 10分钟超时
        print("✅ 当前视频播放结束")
    except Exception as e:
        print(f"❌ 等待视频结束超时或出错: {e}")
        # 即使超时也继续执行

    # 开始按顺序播放推荐视频
    print("\n" + "=" * 60)
    print("开始按顺序播放推荐视频...")
    print("=" * 60)

    for index, video_info in enumerate(url_list):
        try:
            print(f"\n🎬 播放第 {index + 1}/{len(url_list)} 个视频:")
            print(f"📺 标题: {video_info['title']}")
            print(f"🔗 链接: {video_info['url']}")

            # 跳转到下一个视频
            page.goto(video_info['url'])

            # 确保视频元素存在
            page.wait_for_selector("video", timeout=10000)
            print("✅ 视频元素加载完成")

            # 自动播放视频
            try:
                is_paused = page.evaluate("""
                    () => {
                        const video = document.querySelector('video');
                        return video ? video.paused : true;
                    }
                """)
                if is_paused:
                    print("⏸️ 视频处于暂停状态，尝试点击播放")
                    play_button = page.locator(".bpx-player-ctrl-play, .play-btn, [class*='play']").first
                    if play_button.is_visible():
                        play_button.click()
                        print("✅ 点击播放按钮")
                    else:
                        print("⚠️ 播放按钮不可见")
                else:
                    print("▶️ 视频已在播放中，无需操作")
            except:
                print("自动播放未成功，可能视频已自动播放")

            # 等待当前视频播放结束
            print("⏳ 等待视频播放结束...")
            try:
                page.wait_for_function("""
                    () => {
                        const video = document.querySelector('video');
                        return video && video.ended;
                    }
                """, timeout=600000)  # TODO 10分钟超时, 需要修改为更合适的时间
                print("✅ 视频播放结束")
            except Exception as e:
                print(f"❌ 等待视频结束超时: {e}")
                # 即使超时也继续播放下一个
                continue

        except Exception as e:
            print(f"❌ 播放第 {index + 1} 个视频时出错: {e}")
            continue

    print("\n" + "=" * 60)
    print("所有视频播放完成！")
    print("=" * 60)
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)