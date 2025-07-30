#!/usr/bin/env python3
"""
Asynchronous progress display component
Supports timed refresh, fetching progress status from Redis or file
"""

import streamlit as st
import time
from typing import Optional, Dict, Any
from web.utils.async_progress_tracker import get_progress_by_id, format_time

# 导入日志模块
from tradingagents.utils.logging_manager import get_logger
logger = get_logger('async_display')

class AsyncProgressDisplay:
    """Asynchronous progress display component"""
    
    def __init__(self, container, analysis_id: str, refresh_interval: float = 1.0):
        self.container = container
        self.analysis_id = analysis_id
        self.refresh_interval = refresh_interval
        
        # 创建显示组件
        with self.container:
            self.progress_bar = st.progress(0)
            self.status_text = st.empty()
            self.step_info = st.empty()
            self.time_info = st.empty()
            self.refresh_button = st.empty()
        
        # 初始化状态
        self.last_update = 0
        self.is_completed = False
        
        logger.info(f"📊 [Async Display] Initializing: {analysis_id}, Refresh Interval: {refresh_interval}s")
    
    def update_display(self) -> bool:
        """Update display, return whether to continue refreshing"""
        current_time = time.time()
        
        # 检查是否需要刷新
        if current_time - self.last_update < self.refresh_interval and not self.is_completed:
            return not self.is_completed
        
        # 获取进度数据
        progress_data = get_progress_by_id(self.analysis_id)
        
        if not progress_data:
            self.status_text.error("Failed to get analysis progress, please check if the analysis is running")
            return False
        
        # 更新显示
        self._render_progress(progress_data)
        self.last_update = current_time
        
        # 检查是否完成
        status = progress_data.get('status', 'running')
        self.is_completed = status in ['completed', 'failed']
        
        return not self.is_completed
    
    def _render_progress(self, progress_data: Dict[str, Any]):
        """Render progress display"""
        try:
            # 基本信息
            current_step = progress_data.get('current_step', 0)
            total_steps = progress_data.get('total_steps', 8)
            progress_percentage = progress_data.get('progress_percentage', 0.0)
            status = progress_data.get('status', 'running')
            
            # 更新进度条
            self.progress_bar.progress(min(progress_percentage / 100, 1.0))
            
            # 状态信息
            step_name = progress_data.get('current_step_name', 'Unknown')
            step_description = progress_data.get('current_step_description', '')
            last_message = progress_data.get('last_message', '')
            
            # 状态图标
            status_icon = {
                'running': '',
                'completed': '',
                'failed': ''
            }.get(status, '')
            
            # 显示当前状态
            self.status_text.info(f"{status_icon} **Current Status**: {last_message}")
            
            # 显示步骤信息
            if status == 'failed':
                self.step_info.error(f"**Analysis Failed**: {last_message}")
            elif status == 'completed':
                self.step_info.success(f"**Analysis Completed**: All steps completed")

                # 添加查看报告按钮
                with self.step_info:
                    if st.button("View Analysis Report", key=f"view_report_{progress_data.get('analysis_id', 'unknown')}", type="primary"):
                        analysis_id = progress_data.get('analysis_id')
                        # 尝试恢复分析结果（如果还没有的话）
                        if not st.session_state.get('analysis_results'):
                            try:
                                from web.utils.analysis_runner import format_analysis_results
                                raw_results = progress_data.get('raw_results')
                                if raw_results:
                                    formatted_results = format_analysis_results(raw_results)
                                    if formatted_results:
                                        st.session_state.analysis_results = formatted_results
                                        st.session_state.analysis_running = False
                            except Exception as e:
                                st.error(f"Failed to restore analysis results: {e}")

                        # 触发显示报告
                        st.session_state.show_analysis_results = True
                        st.session_state.current_analysis_id = analysis_id
                        st.rerun()
            else:
                self.step_info.info(f"**Progress**: Step {current_step + 1} of {total_steps} ({progress_percentage:.1f}%)\n\n"
                                  f"**Current Step**: {step_name}\n\n"
                                  f"**Step Description**: {step_description}")
            
            # 时间信息 - 实时计算已用时间
            start_time = progress_data.get('start_time', 0)
            estimated_total_time = progress_data.get('estimated_total_time', 0)

            # 计算已用时间
            import time
            if status == 'completed':
                # 已完成的分析使用存储的最终耗时
                real_elapsed_time = progress_data.get('elapsed_time', 0)
            elif start_time > 0:
                # 进行中的分析使用实时计算
                real_elapsed_time = time.time() - start_time
            else:
                # 备用方案
                real_elapsed_time = progress_data.get('elapsed_time', 0)

            # 重新计算剩余时间
            remaining_time = max(estimated_total_time - real_elapsed_time, 0)
            
            if status == 'completed':
                self.time_info.success(f"**Elapsed Time**: {format_time(real_elapsed_time)} | **Total Time**: {format_time(real_elapsed_time)}")
            elif status == 'failed':
                self.time_info.error(f"**Elapsed Time**: {format_time(real_elapsed_time)} | **Analysis Interrupted**")
            else:
                self.time_info.info(f"**Elapsed Time**: {format_time(real_elapsed_time)} | **Estimated Remaining**: {format_time(remaining_time)}")
            
            # 刷新按钮（仅在运行时显示）
            if status == 'running':
                with self.refresh_button:
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        if st.button("Manual Refresh", key=f"refresh_{self.analysis_id}"):
                            st.rerun()
            else:
                self.refresh_button.empty()
                
        except Exception as e:
            logger.error(f"📊 [Async Display] Rendering failed: {e}")
            self.status_text.error(f"❌ Display update failed: {str(e)}")

def create_async_progress_display(container, analysis_id: str, refresh_interval: float = 1.0) -> AsyncProgressDisplay:
    """Create asynchronous progress display component"""
    return AsyncProgressDisplay(container, analysis_id, refresh_interval)

def auto_refresh_progress(display: AsyncProgressDisplay, max_duration: float = 1800):
    """Automatically refresh progress display"""
    start_time = time.time()
    
    # 使用Streamlit的自动刷新机制
    placeholder = st.empty()
    
    while True:
        # 检查超时
        if time.time() - start_time > max_duration:
            with placeholder:
                st.warning("Analysis took too long, auto-refresh stopped. Please manually refresh the page to see the latest status.")
            break
        
        # 更新显示
        should_continue = display.update_display()
        
        if not should_continue:
            # 分析完成或失败，停止刷新
            break
        
        # 等待刷新间隔
        time.sleep(display.refresh_interval)
    
    logger.info(f"📊 [Async Display] Auto-refresh ended: {display.analysis_id}")

# Streamlit专用的自动刷新组件
def streamlit_auto_refresh_progress(analysis_id: str, refresh_interval: int = 2):
    """Streamlit-specific auto-refresh progress display"""

    # 获取进度数据
    progress_data = get_progress_by_id(analysis_id)

    if not progress_data:
        st.error("Failed to get analysis progress, please check if the analysis is running")
        return False

    status = progress_data.get('status', 'running')

    # 基本信息
    current_step = progress_data.get('current_step', 0)
    total_steps = progress_data.get('total_steps', 8)
    progress_percentage = progress_data.get('progress_percentage', 0.0)

    # 进度条
    st.progress(min(progress_percentage / 100, 1.0))

    # 状态信息
    step_name = progress_data.get('current_step_name', 'Unknown')
    step_description = progress_data.get('current_step_description', '')
    last_message = progress_data.get('last_message', '')

    # 状态图标
    status_icon = {
        'running': '🔄',
        'completed': '✅',
        'failed': '❌'
    }.get(status, '🔄')

    # 显示信息
    st.info(f"{status_icon} **Current Status**: {last_message}")

    if status == 'failed':
        st.error(f"❌ **Analysis Failed**: {last_message}")
    elif status == 'completed':
        st.success(f"🎉 **Analysis Completed**: All steps completed")

        # 添加查看报告按钮
        if st.button("View Analysis Report", key=f"view_report_streamlit_{progress_data.get('analysis_id', 'unknown')}", type="primary"):
            analysis_id = progress_data.get('analysis_id')
            # 尝试恢复分析结果（如果还没有的话）
            if not st.session_state.get('analysis_results'):
                try:
                    from web.utils.analysis_runner import format_analysis_results
                    raw_results = progress_data.get('raw_results')
                    if raw_results:
                        formatted_results = format_analysis_results(raw_results)
                        if formatted_results:
                            st.session_state.analysis_results = formatted_results
                            st.session_state.analysis_running = False
                except Exception as e:
                    st.error(f"Failed to restore analysis results: {e}")

            # 触发显示报告
            st.session_state.show_analysis_results = True
            st.session_state.current_analysis_id = analysis_id
            st.rerun()
    else:
        st.info(f"📊 **Progress**: Step {current_step + 1} of {total_steps} ({progress_percentage:.1f}%)\n\n"
               f"**Current Step**: {step_name}\n\n"
               f"**Step Description**: {step_description}")

    # 时间信息 - 实时计算已用时间
    start_time = progress_data.get('start_time', 0)
    estimated_total_time = progress_data.get('estimated_total_time', 0)

    # 计算已用时间
    import time
    if status == 'completed':
        # 已完成的分析使用存储的最终耗时
        elapsed_time = progress_data.get('elapsed_time', 0)
    elif start_time > 0:
        # 进行中的分析使用实时计算
        elapsed_time = time.time() - start_time
    else:
        # 备用方案
        elapsed_time = progress_data.get('elapsed_time', 0)

    # 重新计算剩余时间
    remaining_time = max(estimated_total_time - elapsed_time, 0)

    if status == 'completed':
        st.success(f"⏱️ **Total Time**: {format_time(elapsed_time)}")
    elif status == 'failed':
        st.error(f"⏱️ **Elapsed Time**: {format_time(elapsed_time)} | **Analysis Interrupted**")
    else:
        st.info(f"⏱️ **Elapsed Time**: {format_time(elapsed_time)} | **Estimated Remaining**: {format_time(remaining_time)}")

    # 添加刷新控制（仅在运行时显示）
    if status == 'running':
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔄 Refresh Progress", key=f"refresh_streamlit_{analysis_id}"):
                st.rerun()
        with col2:
            auto_refresh_key = f"auto_refresh_streamlit_{analysis_id}"
            # 获取默认值，如果是新分析则默认为True
            default_value = st.session_state.get(auto_refresh_key, True)  # 默认为True
            auto_refresh = st.checkbox("🔄 Auto-refresh", value=default_value, key=auto_refresh_key)
            if auto_refresh and status == 'running':  # 只在运行时自动刷新
                import time
                time.sleep(3)  # 等待3秒
                st.rerun()
            elif auto_refresh and status in ['completed', 'failed']:
                # 分析完成后自动关闭自动刷新
                st.session_state[auto_refresh_key] = False

    return status in ['completed', 'failed']

# 新增：静态进度显示（不会触发页面刷新）
def display_static_progress(analysis_id: str) -> bool:
    """
    Display static progress (does not auto-refresh)
    Returns whether it is completed
    """
    import streamlit as st

    # 使用session state避免重复创建组件
    progress_key = f"progress_display_{analysis_id}"
    if progress_key not in st.session_state:
        st.session_state[progress_key] = True

    # 获取进度数据
    progress_data = get_progress_by_id(analysis_id)

    if not progress_data:
        st.error("❌ Failed to get analysis progress, please check if the analysis is running")
        return False

    status = progress_data.get('status', 'running')

    # 调试信息（可以在生产环境中移除）
    import datetime
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    logger.debug(f"📊 [Progress Display] {current_time} - Status: {status}, Progress: {progress_data.get('progress_percentage', 0):.1f}%")

    # 显示基本信息（移除分析ID显示）
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

    with col1:
        step_name = progress_data.get('current_step_name', 'Unknown')
        st.write(f"**Current Step**: {step_name}")

    with col2:
        progress_percentage = progress_data.get('progress_percentage', 0.0)
        st.metric("Progress", f"{progress_percentage:.1f}%")

    with col3:
        # 计算已用时间
        start_time = progress_data.get('start_time', 0)
        import time
        if status == 'completed':
            # 已完成的分析使用存储的最终耗时
            elapsed_time = progress_data.get('elapsed_time', 0)
        elif start_time > 0:
            # 进行中的分析使用实时计算
            elapsed_time = time.time() - start_time
        else:
            # 备用方案
            elapsed_time = progress_data.get('elapsed_time', 0)
        st.metric("Elapsed Time", format_time(elapsed_time))

    with col4:
        remaining_time = progress_data.get('remaining_time', 0)
        if status == 'completed':
            st.metric("Estimated Remaining", "Completed")
        elif status == 'failed':
            st.metric("Estimated Remaining", "Interrupted")
        elif remaining_time > 0 and status == 'running':
            st.metric("Estimated Remaining", format_time(remaining_time))
        else:
            st.metric("Estimated Remaining", "Calculating...")

    # 进度条
    st.progress(min(progress_percentage / 100, 1.0))

    # 步骤详情
    step_description = progress_data.get('current_step_description', 'Processing...')
    st.write(f"**Current Task**: {step_description}")

    # 状态信息
    last_message = progress_data.get('last_message', '')

    # 状态图标
    status_icon = {
        'running': '🔄',
        'completed': '✅',
        'failed': '❌'
    }.get(status, '🔄')

    # 显示状态
    if status == 'failed':
        st.error(f"❌ **Analysis Failed**: {last_message}")
    elif status == 'completed':
        st.success(f"🎉 **Analysis Completed**: {last_message}")

        # 添加查看报告按钮
        if st.button("View Analysis Report", key=f"view_report_static_{analysis_id}", type="primary"):
            # 尝试恢复分析结果（如果还没有的话）
            if not st.session_state.get('analysis_results'):
                try:
                    from web.utils.async_progress_tracker import get_progress_by_id
                    from web.utils.analysis_runner import format_analysis_results
                    progress_data = get_progress_by_id(analysis_id)
                    if progress_data and progress_data.get('raw_results'):
                        formatted_results = format_analysis_results(progress_data['raw_results'])
                        if formatted_results:
                            st.session_state.analysis_results = formatted_results
                            st.session_state.analysis_running = False
                except Exception as e:
                    st.error(f"Failed to restore analysis results: {e}")

            # 触发显示报告
            st.session_state.show_analysis_results = True
            st.session_state.current_analysis_id = analysis_id
            st.rerun()
    else:
        st.info(f"{status_icon} **Current Status**: {last_message}")

        # 添加刷新控制（仅在运行时显示）
        if status == 'running':
            # 使用唯一的容器避免重复
            refresh_container_key = f"refresh_container_{analysis_id}"
            if refresh_container_key not in st.session_state:
                st.session_state[refresh_container_key] = True

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🔄 Refresh Progress", key=f"refresh_static_{analysis_id}"):
                    st.rerun()
            with col2:
                auto_refresh_key = f"auto_refresh_static_{analysis_id}"
                # 获取默认值，如果是新分析则默认为True
                default_value = st.session_state.get(auto_refresh_key, True)  # 默认为True
                auto_refresh = st.checkbox("🔄 Auto-refresh", value=default_value, key=auto_refresh_key)
                if auto_refresh and status == 'running':  # 只在运行时自动刷新
                    import time
                    time.sleep(3)  # 等待3秒
                    st.rerun()
                elif auto_refresh and status in ['completed', 'failed']:
                    # 分析完成后自动关闭自动刷新
                    st.session_state[auto_refresh_key] = False

    # 清理session state（分析完成后）
    if status in ['completed', 'failed']:
        progress_key = f"progress_display_{analysis_id}"
        refresh_container_key = f"refresh_container_{analysis_id}"
        if progress_key in st.session_state:
            del st.session_state[progress_key]
        if refresh_container_key in st.session_state:
            del st.session_state[refresh_container_key]

    return status in ['completed', 'failed']


def display_unified_progress(analysis_id: str, show_refresh_controls: bool = True) -> bool:
    """
    Unified progress display function to avoid duplicate elements
    Returns whether it is completed
    """
    import streamlit as st

    # 简化逻辑：直接调用显示函数，通过参数控制是否显示刷新按钮
    # 调用方负责确保只在需要的地方传入show_refresh_controls=True
    return display_static_progress_with_controls(analysis_id, show_refresh_controls)


def display_static_progress_with_controls(analysis_id: str, show_refresh_controls: bool = True) -> bool:
    """
    Display static progress, with control over whether to show refresh controls
    """
    import streamlit as st
    from web.utils.async_progress_tracker import get_progress_by_id

    # 获取进度数据
    progress_data = get_progress_by_id(analysis_id)

    if not progress_data:
        # 如果没有进度数据，显示默认的准备状态
        st.info("🔄 **Current Status**: Ready to start analysis...")

        # 如果需要显示刷新控件，仍然显示
        if show_refresh_controls:
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🔄 Refresh Progress", key=f"refresh_unified_default_{analysis_id}"):
                    st.rerun()
            with col2:
                auto_refresh_key = f"auto_refresh_unified_default_{analysis_id}"
                # 获取默认值，如果是新分析则默认为True
                default_value = st.session_state.get(auto_refresh_key, True)  # 默认为True
                auto_refresh = st.checkbox("🔄 Auto-refresh", value=default_value, key=auto_refresh_key)
                if auto_refresh and status == 'running':  # 只在运行时自动刷新
                    import time
                    time.sleep(3)  # 等待3秒
                    st.rerun()
                elif auto_refresh and status in ['completed', 'failed']:
                    # 分析完成后自动关闭自动刷新
                    st.session_state[auto_refresh_key] = False

        return False  # 返回False表示还未完成

    # 解析进度数据（修复字段名称匹配）
    status = progress_data.get('status', 'running')
    current_step = progress_data.get('current_step', 0)
    current_step_name = progress_data.get('current_step_name', 'Initialization Phase')
    progress_percentage = progress_data.get('progress_percentage', 0.0)

    # 计算已用时间
    start_time = progress_data.get('start_time', 0)
    estimated_total_time = progress_data.get('estimated_total_time', 0)
    import time
    if status == 'completed':
        # 已完成的分析使用存储的最终耗时
        elapsed_time = progress_data.get('elapsed_time', 0)
    elif start_time > 0:
        # 进行中的分析使用实时计算
        elapsed_time = time.time() - start_time
    else:
        # 备用方案
        elapsed_time = progress_data.get('elapsed_time', 0)

    # 重新计算剩余时间
    remaining_time = max(estimated_total_time - elapsed_time, 0)
    current_step_description = progress_data.get('current_step_description', 'Initializing analysis engine')
    last_message = progress_data.get('last_message', 'Ready to start analysis')

    # 显示当前步骤
    st.write(f"**Current Step**: {current_step_name}")

    # 显示进度条和统计信息
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Progress", f"{progress_percentage:.1f}%")

    with col2:
        st.metric("Elapsed Time", format_time(elapsed_time))

    with col3:
        if status == 'completed':
            st.metric("Estimated Remaining", "Completed")
        elif status == 'failed':
            st.metric("Estimated Remaining", "Interrupted")
        else:
            st.metric("Estimated Remaining", format_time(remaining_time))

    # 显示进度条
    st.progress(min(progress_percentage / 100.0, 1.0))

    # 显示当前任务
    st.write(f"**Current Task**: {current_step_description}")

    # 显示当前状态
    status_icon = {
        'running': '🔄',
        'completed': '✅',
        'failed': '❌'
    }.get(status, '🔄')

    if status == 'completed':
        st.success(f"{status_icon} **Current Status**: {last_message}")

        # 添加查看报告按钮
        if st.button("View Analysis Report", key=f"view_report_unified_{analysis_id}", type="primary"):
            # 尝试恢复分析结果（如果还没有的话）
            if not st.session_state.get('analysis_results'):
                try:
                    from web.utils.async_progress_tracker import get_progress_by_id
                    from web.utils.analysis_runner import format_analysis_results
                    progress_data = get_progress_by_id(analysis_id)
                    if progress_data and progress_data.get('raw_results'):
                        formatted_results = format_analysis_results(progress_data['raw_results'])
                        if formatted_results:
                            st.session_state.analysis_results = formatted_results
                            st.session_state.analysis_running = False
                except Exception as e:
                    st.error(f"Failed to restore analysis results: {e}")

            # 触发显示报告
            st.session_state.show_analysis_results = True
            st.session_state.current_analysis_id = analysis_id
            st.rerun()
    elif status == 'failed':
        st.error(f"{status_icon} **Current Status**: {last_message}")
    else:
        st.info(f"{status_icon} **Current Status**: {last_message}")

    # 显示刷新控制的条件：
    # 1. 需要显示刷新控件 AND
    # 2. (分析正在运行 OR 分析刚开始还没有状态)
    if show_refresh_controls and (status == 'running' or status == 'initializing'):
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔄 Refresh Progress", key=f"refresh_unified_{analysis_id}"):
                st.rerun()
        with col2:
            auto_refresh_key = f"auto_refresh_unified_{analysis_id}"
            # 获取默认值，如果是新分析则默认为True
            default_value = st.session_state.get(auto_refresh_key, True)  # 默认为True
            auto_refresh = st.checkbox("🔄 Auto-refresh", value=default_value, key=auto_refresh_key)
            if auto_refresh and status == 'running':  # 只在运行时自动刷新
                import time
                time.sleep(3)  # 等待3秒
                st.rerun()
            elif auto_refresh and status in ['completed', 'failed']:
                # 分析完成后自动关闭自动刷新
                st.session_state[auto_refresh_key] = False

    # 不需要清理session state，因为我们通过参数控制显示

    return status in ['completed', 'failed']
