USE [STG]
GO
/****** Object:  Table [dbo].[current_weather]    Script Date: 4/29/2024 10:54:52 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[current_weather](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[location_id] [int] NULL,
	[dt] [bigint] NULL,
	[sunrise] [bigint] NULL,
	[sunset] [bigint] NULL,
	[temp] [decimal](5, 2) NULL,
	[feels_like] [decimal](5, 2) NULL,
	[pressure] [int] NULL,
	[humidity] [int] NULL,
	[dew_point] [decimal](5, 2) NULL,
	[uvi] [decimal](3, 2) NULL,
	[clouds] [int] NULL,
	[visibility] [int] NULL,
	[wind_speed] [decimal](5, 2) NULL,
	[wind_deg] [int] NULL,
	[wind_gust] [decimal](5, 2) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[locations]    Script Date: 4/29/2024 10:54:52 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[locations](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[latitude] [decimal](10, 6) NULL,
	[longitude] [decimal](10, 6) NULL,
	[timezone] [varchar](50) NULL,
	[timezone_offset] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[rain]    Script Date: 4/29/2024 10:54:52 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[rain](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[current_weather_id] [int] NULL,
	[rain_1h] [decimal](6, 2) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[weather_descriptions]    Script Date: 4/29/2024 10:54:52 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[weather_descriptions](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[current_weather_id] [int] NULL,
	[weather_id] [int] NULL,
	[main] [varchar](50) NULL,
	[description] [varchar](100) NULL,
	[icon] [varchar](10) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[current_weather]  WITH CHECK ADD FOREIGN KEY([location_id])
REFERENCES [dbo].[locations] ([id])
GO
ALTER TABLE [dbo].[rain]  WITH CHECK ADD FOREIGN KEY([current_weather_id])
REFERENCES [dbo].[current_weather] ([id])
GO
ALTER TABLE [dbo].[weather_descriptions]  WITH CHECK ADD FOREIGN KEY([current_weather_id])
REFERENCES [dbo].[current_weather] ([id])
GO
