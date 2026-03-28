import { scaleTime, scaleLinear } from 'd3-scale';
import { axisBottom } from 'd3-axis';
import { select } from 'd3-selection';
import { timeYear, timeMonth } from 'd3-time';
import { timeFormat } from 'd3-time-format';
import { extent, groups } from 'd3-array';

export interface TimelineEvent {
  id: string;
  title: string;
  date: string;
  end_date: string | null;
  dependency: string;
  event_type: string;
  severity: string;
  summary: string;
  artworkCount: number;
}

interface ParsedEvent extends TimelineEvent {
  startDate: Date;
  endDate: Date | null;
  isRange: boolean;
}

function parseDate(s: string): Date {
  if (/^\d{4}$/.test(s)) return new Date(`${s}-07-01T00:00:00Z`);
  if (/^\d{4}-\d{2}$/.test(s)) return new Date(`${s}-15T00:00:00Z`);
  return new Date(`${s}T00:00:00Z`);
}

function getCSSVar(name: string): string {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function severityColor(severity: string): string {
  switch (severity) {
    case 'total': return getCSSVar('--severity-total');
    case 'major': return getCSSVar('--severity-major');
    case 'minor': return getCSSVar('--severity-minor');
    default: return getCSSVar('--timeline-track');
  }
}

export function initTimeline(container: HTMLElement, data: TimelineEvent[]): void {
  if (data.length === 0) {
    container.innerHTML = '<p style="color: var(--text-muted); text-align: center; padding: 2rem;">No events to display.</p>';
    return;
  }

  const allParsed: ParsedEvent[] = data.map((d) => ({
    ...d,
    startDate: parseDate(d.date),
    endDate: d.end_date ? parseDate(d.end_date) : null,
    isRange: !!d.end_date,
  }));

  let activeFilter = 'all';

  document.addEventListener('timeline:filter', ((e: CustomEvent) => {
    activeFilter = e.detail.filter;
    resetZoom();
    render();
  }) as EventListener);

  const margin = { top: 20, right: 30, bottom: 40, left: 30 };
  const height = 220;

  // Zoom/pan state
  let fullDomain: [Date, Date] = [new Date(), new Date()];
  let viewDomain: [Date, Date] = [new Date(), new Date()];
  let isPanning = false;
  let panStartX = 0;
  let panStartDomain: [Date, Date] = [new Date(), new Date()];
  let pinchStartDist = 0;
  let pinchMidX = 0;
  let pinchStartDomain: [Date, Date] = [new Date(), new Date()];
  const isMobile = 'ontouchstart' in window;

  function resetZoom() {
    viewDomain = [...fullDomain] as [Date, Date];
  }

  function clampDomain(domain: [Date, Date]): [Date, Date] {
    const fullSpan = fullDomain[1].getTime() - fullDomain[0].getTime();
    const minSpan = fullSpan * 0.02; // max zoom: ~2% of full range
    let [start, end] = domain;
    let span = end.getTime() - start.getTime();

    if (span < minSpan) {
      const mid = start.getTime() + span / 2;
      start = new Date(mid - minSpan / 2);
      end = new Date(mid + minSpan / 2);
      span = minSpan;
    }

    if (span > fullSpan) {
      return [...fullDomain] as [Date, Date];
    }

    if (start.getTime() < fullDomain[0].getTime()) {
      start = fullDomain[0];
      end = new Date(start.getTime() + span);
    }
    if (end.getTime() > fullDomain[1].getTime()) {
      end = fullDomain[1];
      start = new Date(end.getTime() - span);
    }

    return [start, end];
  }

  function render() {
    container.innerHTML = '';

    const parsed = activeFilter === 'all'
      ? allParsed
      : allParsed.filter(d => d.event_type === activeFilter);

    if (parsed.length === 0) {
      container.innerHTML = '<p style="color: var(--text-muted); text-align: center; padding: 2rem;">No events match this filter.</p>';
      return;
    }

    const containerWidth = container.clientWidth;
    if (containerWidth === 0) return;
    const width = containerWidth;
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const allDates = parsed.flatMap((d) => d.endDate ? [d.startDate, d.endDate] : [d.startDate]);
    const [minDate, maxDate] = extent(allDates) as [Date, Date];

    const padMs = (maxDate.getTime() - minDate.getTime()) * 0.05;
    fullDomain = [new Date(minDate.getTime() - padMs), new Date(maxDate.getTime() + padMs)];

    // Only reset view if it's the initial render or filter changed
    if (viewDomain[0].getTime() === viewDomain[1].getTime()) {
      viewDomain = [...fullDomain] as [Date, Date];
    }

    const x = scaleTime()
      .domain(viewDomain)
      .range([0, innerWidth]);

    const svg = select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('role', 'img')
      .attr('aria-label', 'Timeline of net art extinction events')
      .style('touch-action', 'none');

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Determine tick interval based on visible span
    const visibleSpanYears = (viewDomain[1].getTime() - viewDomain[0].getTime()) / (365.25 * 24 * 60 * 60 * 1000);
    let tickInterval;
    let tickFormatStr = '%Y';
    if (visibleSpanYears <= 2) {
      tickInterval = timeMonth.every(3)!;
      tickFormatStr = '%b %Y';
    } else if (visibleSpanYears <= 5) {
      tickInterval = timeYear.every(1)!;
    } else if (visibleSpanYears <= 15) {
      tickInterval = timeYear.every(2)!;
    } else {
      tickInterval = timeYear.every(5)!;
    }

    // Gridlines
    const trackColor = getCSSVar('--timeline-track');
    const borderColor = getCSSVar('--border');
    const gridTicks = x.ticks(tickInterval);

    g.selectAll('.gridline')
      .data(gridTicks)
      .join('line')
      .attr('class', 'gridline')
      .attr('x1', (d: Date) => x(d))
      .attr('x2', (d: Date) => x(d))
      .attr('y1', 0)
      .attr('y2', innerHeight)
      .attr('stroke', borderColor)
      .attr('stroke-dasharray', '2,4')
      .attr('stroke-width', 0.5);

    // Axis
    const textColor = getCSSVar('--text-muted');
    const xAxis = axisBottom(x)
      .ticks(tickInterval)
      .tickFormat((d) => timeFormat(tickFormatStr)(d as Date))
      .tickSizeOuter(0);

    const axisG = g.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(xAxis);

    axisG.selectAll('text').attr('fill', textColor).attr('font-size', '11px');
    axisG.selectAll('line').attr('stroke', trackColor);
    axisG.select('.domain').attr('stroke', trackColor);

    // Track line
    g.append('line')
      .attr('x1', 0)
      .attr('x2', innerWidth)
      .attr('y1', innerHeight / 2)
      .attr('y2', innerHeight / 2)
      .attr('stroke', trackColor)
      .attr('stroke-width', 1.5);

    // Filter to visible events only
    const visibleParsed = parsed.filter((d) => {
      const endDate = d.endDate ?? d.startDate;
      return endDate >= viewDomain[0] && d.startDate <= viewDomain[1];
    });

    // Layout: avoid overlap by assigning vertical lanes
    const sortedEvents = [...visibleParsed].sort((a, b) => a.startDate.getTime() - b.startDate.getTime());
    const lanes: { endX: number }[] = [];

    const laneAssignment = sortedEvents.map((evt) => {
      const sx = x(evt.startDate);
      const ex = evt.endDate ? x(evt.endDate) : sx + 10;
      let lane = lanes.findIndex((l) => l.endX < sx - 8);
      if (lane === -1) {
        lane = lanes.length;
        lanes.push({ endX: 0 });
      }
      lanes[lane].endX = ex;
      return { event: evt, lane };
    });

    const laneCount = Math.max(lanes.length, 1);
    const laneHeight = Math.min(30, (innerHeight - 20) / laneCount);
    const baseY = innerHeight / 2 - (laneCount * laneHeight) / 2;

    // Tooltip — reuse existing or create
    const tooltipParent = container.parentElement ?? container;
    let tooltipNode = tooltipParent.querySelector('.timeline-tooltip') as HTMLElement | null;
    if (!tooltipNode) {
      tooltipNode = document.createElement('div');
      tooltipNode.className = 'timeline-tooltip';
      tooltipNode.style.opacity = '0';
      tooltipParent.appendChild(tooltipNode);
    }
    tooltipNode.style.opacity = '0';
    const tooltip = select(tooltipNode);

    // Range events (bars)
    const rangeEvents = laneAssignment.filter(({ event }) => event.isRange);
    g.selectAll('.range-bar')
      .data(rangeEvents)
      .join('rect')
      .attr('class', 'range-bar')
      .attr('x', ({ event }) => x(event.startDate))
      .attr('y', ({ lane }) => baseY + lane * laneHeight + laneHeight * 0.2)
      .attr('width', ({ event }) => Math.max(4, x(event.endDate!) - x(event.startDate)))
      .attr('height', laneHeight * 0.6)
      .attr('rx', 3)
      .attr('fill', ({ event }) => severityColor(event.severity))
      .attr('opacity', 0.35)
      .attr('cursor', 'pointer')
      .on('mouseenter', function (_e: MouseEvent, { event }: { event: ParsedEvent }) {
        select(this).attr('opacity', 0.6);
        showTooltip(event, _e);
      })
      .on('mousemove', function (_e: MouseEvent) {
        moveTooltip(_e);
      })
      .on('mouseleave', function () {
        select(this).attr('opacity', 0.35);
        hideTooltip();
      })
      .on('click', (_e: MouseEvent, { event }: { event: ParsedEvent }) => {
        window.location.href = `/events/${event.id}`;
      });

    // Point events (circles)
    const pointEvents = laneAssignment.filter(({ event }) => !event.isRange);
    const maxArtworks = Math.max(1, ...pointEvents.map(({ event }) => event.artworkCount));
    const rScale = scaleLinear().domain([0, maxArtworks]).range([5, 14]);

    g.selectAll('.point-dot')
      .data(pointEvents)
      .join('circle')
      .attr('class', 'point-dot')
      .attr('cx', ({ event }) => x(event.startDate))
      .attr('cy', ({ lane }) => baseY + lane * laneHeight + laneHeight / 2)
      .attr('r', ({ event }) => rScale(event.artworkCount))
      .attr('fill', ({ event }) => severityColor(event.severity))
      .attr('stroke', getCSSVar('--bg'))
      .attr('stroke-width', 2)
      .attr('cursor', 'pointer')
      .on('mouseenter', function (_e: MouseEvent, { event }: { event: ParsedEvent }) {
        select(this).attr('r', (rScale(event.artworkCount) as number) * 1.3);
        showTooltip(event, _e);
      })
      .on('mousemove', function (_e: MouseEvent) {
        moveTooltip(_e);
      })
      .on('mouseleave', function (_e: MouseEvent, { event }: { event: ParsedEvent }) {
        select(this).attr('r', rScale(event.artworkCount) as number);
        hideTooltip();
      })
      .on('click', (_e: MouseEvent, { event }: { event: ParsedEvent }) => {
        window.location.href = `/events/${event.id}`;
      });

    // Touch: tap on dot/bar shows tooltip, tap elsewhere hides
    if (isMobile) {
      let activeTouch: ParsedEvent | null = null;

      const handleTap = (event: ParsedEvent, el: SVGElement, e: TouchEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (activeTouch === event) {
          // Second tap navigates
          window.location.href = `/events/${event.id}`;
          return;
        }
        activeTouch = event;
        const touch = e.changedTouches[0];
        const fakeMouseEvent = { clientX: touch.clientX, clientY: touch.clientY } as MouseEvent;
        showTooltip(event, fakeMouseEvent);
      };

      g.selectAll<SVGCircleElement, { event: ParsedEvent }>('.point-dot')
        .on('touchend', function (e: TouchEvent, { event }: { event: ParsedEvent }) {
          handleTap(event, this, e);
        });

      g.selectAll<SVGRectElement, { event: ParsedEvent }>('.range-bar')
        .on('touchend', function (e: TouchEvent, { event }: { event: ParsedEvent }) {
          handleTap(event, this, e);
        });

      svg.on('touchend', (e: TouchEvent) => {
        if (e.target === svg.node() || (e.target as Element).tagName === 'line') {
          activeTouch = null;
          hideTooltip();
        }
      });
    }

    // Zoom/pan interaction on SVG
    const svgNode = svg.node()!;

    // Mouse wheel zoom (desktop)
    svgNode.addEventListener('wheel', (e: WheelEvent) => {
      e.preventDefault();
      const rect = svgNode.getBoundingClientRect();
      const mouseX = e.clientX - rect.left - margin.left;
      const fraction = mouseX / innerWidth;

      const span = viewDomain[1].getTime() - viewDomain[0].getTime();
      const zoomFactor = e.deltaY > 0 ? 1.15 : 0.85;
      const newSpan = span * zoomFactor;

      const mouseTime = viewDomain[0].getTime() + span * fraction;
      const newStart = mouseTime - newSpan * fraction;
      const newEnd = newStart + newSpan;

      viewDomain = clampDomain([new Date(newStart), new Date(newEnd)]);
      render();
    }, { passive: false });

    // Touch pan & pinch zoom
    svgNode.addEventListener('touchstart', (e: TouchEvent) => {
      if (e.touches.length === 1) {
        isPanning = true;
        panStartX = e.touches[0].clientX;
        panStartDomain = [...viewDomain] as [Date, Date];
      } else if (e.touches.length === 2) {
        isPanning = false;
        const dx = e.touches[1].clientX - e.touches[0].clientX;
        const dy = e.touches[1].clientY - e.touches[0].clientY;
        pinchStartDist = Math.sqrt(dx * dx + dy * dy);
        pinchMidX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
        pinchStartDomain = [...viewDomain] as [Date, Date];
        hideTooltip();
      }
    }, { passive: true });

    svgNode.addEventListener('touchmove', (e: TouchEvent) => {
      if (e.touches.length === 1 && isPanning) {
        e.preventDefault();
        const dx = e.touches[0].clientX - panStartX;
        const pxPerMs = innerWidth / (panStartDomain[1].getTime() - panStartDomain[0].getTime());
        const shiftMs = -dx / pxPerMs;
        const newStart = new Date(panStartDomain[0].getTime() + shiftMs);
        const newEnd = new Date(panStartDomain[1].getTime() + shiftMs);
        viewDomain = clampDomain([newStart, newEnd]);
        render();
      } else if (e.touches.length === 2) {
        e.preventDefault();
        const dx = e.touches[1].clientX - e.touches[0].clientX;
        const dy = e.touches[1].clientY - e.touches[0].clientY;
        const dist = Math.sqrt(dx * dx + dy * dy);
        const scale = pinchStartDist / dist;

        const rect = svgNode.getBoundingClientRect();
        const midX = pinchMidX - rect.left - margin.left;
        const fraction = midX / innerWidth;

        const oldSpan = pinchStartDomain[1].getTime() - pinchStartDomain[0].getTime();
        const newSpan = oldSpan * scale;
        const midTime = pinchStartDomain[0].getTime() + oldSpan * fraction;
        const newStart = midTime - newSpan * fraction;
        const newEnd = newStart + newSpan;

        viewDomain = clampDomain([new Date(newStart), new Date(newEnd)]);
        render();
      }
    }, { passive: false });

    svgNode.addEventListener('touchend', () => {
      isPanning = false;
    }, { passive: true });

    function showTooltip(event: ParsedEvent, e: MouseEvent) {
      tooltip
        .html(`
          <strong>${event.title}</strong><br/>
          <span class="tooltip-dep">${event.dependency}</span><br/>
          <span class="tooltip-date">${event.date}${event.end_date ? ' — ' + event.end_date : ''}</span><br/>
          <span class="tooltip-summary">${event.summary}</span>
        `)
        .style('opacity', 1);
      moveTooltip(e);
    }

    function moveTooltip(e: MouseEvent) {
      const rect = tooltipParent.getBoundingClientRect();
      let left = e.clientX - rect.left + 12;
      let top = e.clientY - rect.top - 10;
      const tw = Math.min(280, rect.width - 24);
      tooltip.style('max-width', tw + 'px');
      if (left + tw > rect.width) left = left - tw - 24;
      if (left < 0) left = 8;
      tooltip.style('left', left + 'px').style('top', top + 'px');
    }

    function hideTooltip() {
      tooltip.style('opacity', 0);
    }
  }

  render();

  // Add zoom controls for mobile
  if (isMobile) {
    const controls = document.createElement('div');
    controls.className = 'timeline-controls';
    controls.innerHTML = `
      <button class="timeline-ctrl" id="tl-zoom-in" aria-label="Zoom in">+</button>
      <button class="timeline-ctrl" id="tl-zoom-out" aria-label="Zoom out">&minus;</button>
      <button class="timeline-ctrl" id="tl-reset" aria-label="Reset zoom">Reset</button>
    `;
    (container.parentElement ?? container).appendChild(controls);

    document.getElementById('tl-zoom-in')!.addEventListener('click', () => {
      const span = viewDomain[1].getTime() - viewDomain[0].getTime();
      const mid = viewDomain[0].getTime() + span / 2;
      const newSpan = span * 0.6;
      viewDomain = clampDomain([new Date(mid - newSpan / 2), new Date(mid + newSpan / 2)]);
      render();
    });

    document.getElementById('tl-zoom-out')!.addEventListener('click', () => {
      const span = viewDomain[1].getTime() - viewDomain[0].getTime();
      const mid = viewDomain[0].getTime() + span / 2;
      const newSpan = span * 1.6;
      viewDomain = clampDomain([new Date(mid - newSpan / 2), new Date(mid + newSpan / 2)]);
      render();
    });

    document.getElementById('tl-reset')!.addEventListener('click', () => {
      resetZoom();
      render();
    });
  }

  const ro = new ResizeObserver(() => render());
  ro.observe(container);
}
