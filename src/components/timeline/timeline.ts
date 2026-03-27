import { scaleTime, scaleLinear } from 'd3-scale';
import { axisBottom } from 'd3-axis';
import { select } from 'd3-selection';
import { timeYear } from 'd3-time';
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

  const parsed: ParsedEvent[] = data.map((d) => ({
    ...d,
    startDate: parseDate(d.date),
    endDate: d.end_date ? parseDate(d.end_date) : null,
    isRange: !!d.end_date,
  }));

  const margin = { top: 20, right: 30, bottom: 40, left: 30 };
  const height = 220;

  function render() {
    container.innerHTML = '';

    const containerWidth = container.clientWidth;
    if (containerWidth === 0) return;
    const width = containerWidth;
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const allDates = parsed.flatMap((d) => d.endDate ? [d.startDate, d.endDate] : [d.startDate]);
    const [minDate, maxDate] = extent(allDates) as [Date, Date];

    const padMs = (maxDate.getTime() - minDate.getTime()) * 0.05;
    const x = scaleTime()
      .domain([new Date(minDate.getTime() - padMs), new Date(maxDate.getTime() + padMs)])
      .range([0, innerWidth]);

    const svg = select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('role', 'img')
      .attr('aria-label', 'Timeline of net art extinction events');

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Gridlines
    const trackColor = getCSSVar('--timeline-track');
    const borderColor = getCSSVar('--border');
    const yearTicks = x.ticks(timeYear.every(1)!);

    g.selectAll('.gridline')
      .data(yearTicks)
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
      .ticks(timeYear.every(1)!)
      .tickFormat((d) => timeFormat('%Y')(d as Date))
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

    // Layout: avoid overlap by assigning vertical lanes
    const sortedEvents = [...parsed].sort((a, b) => a.startDate.getTime() - b.startDate.getTime());
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

    // Tooltip — append to parent .timeline-container to avoid overflow:hidden clipping
    const tooltipParent = container.parentElement ?? container;
    const tooltip = select(tooltipParent)
      .append('div')
      .attr('class', 'timeline-tooltip')
      .style('opacity', 0);

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
      .on('mousemove', function (_e: MouseEvent, { event }: { event: ParsedEvent }) {
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
      const tw = 280;
      if (left + tw > rect.width) left = left - tw - 24;
      tooltip.style('left', left + 'px').style('top', top + 'px');
    }

    function hideTooltip() {
      tooltip.style('opacity', 0);
    }
  }

  render();

  const ro = new ResizeObserver(() => render());
  ro.observe(container);
}
