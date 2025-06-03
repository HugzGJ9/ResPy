from API.SUPABASE.save import saveDailyGenerationTS
from Reporting.buildGenerationReport import buildMonthlyTable, buildGenerationForecastEmail, fetchGenerationReport
from API.SUPABASE.data import fetchRESGenerationMonthlyData
from Model.ResPowerGeneration.RESPowerGeneration_forecast import getGenerationForecastReport

generation_forecast = getGenerationForecastReport(model_name="model_RES_generation_LGBMR_cleaned_pt")

res_generation_month, res_generation_day = fetchRESGenerationMonthlyData("FR")
monthly_stats = buildMonthlyTable(res_generation_month, res_generation_day)
saveDailyGenerationTS(generation_forecast, 'HUGO')

tables, image_cid, img_data = fetchGenerationReport(generation_forecast, monthly_stats)
title = f'Hugo RES Generation Forecast FR {generation_forecast.index[0].strftime("%Y-%m-%d")}'

buildGenerationForecastEmail(title=title, tables=tables, image_cid=image_cid, img_data=img_data)