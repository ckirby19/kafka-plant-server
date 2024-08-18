import HighchartsReact from "highcharts-react-official";
import Highcharts, { PointOptionsObject, SeriesOptionsType } from "highcharts/highstock"
import { Data } from "../model";

export interface DataDisplayProps {
    Data: Record<string, Data[]>;
}

const generateLineData = (lines: Data[]): PointOptionsObject[] => 
    lines.map((line) => {
        const lineValue = line.Value;
        return ({
            x: line.Timestamp,
            y: lineValue
        })
    }).sort((one, two) => one.x - two.x)

const seriesConfig = (data: Data[], i: number) => {return {type: "line", yAxis: `line${i}`, data: generateLineData(data)} };

const generateSeries = (data: Record<string, Data[]>): SeriesOptionsType[] => 
    Object.entries(data).map(([k, data], i) => {
        const config = seriesConfig(data, i);
        return {
            type: config.type,
            name: k,
            yAxis: config.yAxis,
            color: "red",
            data: config.data
        } as SeriesOptionsType
    })

const useChartOptions = (data: Record<string, Data[]>) => {
    const seriesData = [generateSeries(data)]
    return chartOptions(seriesData.flat())
}

const chartOptions = (series: SeriesOptionsType[]): Highcharts.Options => {
    return {
        chart: {
            animation: true,
            backgroundColor: "transparent"
        },
        time: {
            useUTC: false
        },
        plotOptions: {
            line: {
                marker: {
                    enabled: true,
                    symbol: "circle",
                    radius: 5
                }
            }
        },
        series: series
    }
}



export const DataDisplay = ({ Data }: DataDisplayProps) => {
    const chartOptions = useChartOptions(Data)
    return (
        <HighchartsReact
            highcharts={Highcharts}
            constructorType={"stockChart"}
            options={chartOptions}
        />
    )
}