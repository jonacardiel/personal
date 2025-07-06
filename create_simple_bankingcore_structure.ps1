$root = "c:\Users\NoBinario\Documents\personal\SimpleBankingCore"

# Core
New-Item -ItemType Directory -Path "$root\SimpleBankingCore.Core\Models" -Force
New-Item -ItemType Directory -Path "$root\SimpleBankingCore.Core\Enums" -Force
New-Item -ItemType Directory -Path "$root\SimpleBankingCore.Core\Exceptions" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Core\Models\Account.cs" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Core\Models\Customer.cs" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Core\Models\Transaction.cs" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Core\Enums\AccountType.cs" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Core\Enums\TransactionType.cs" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Core\Exceptions\InsufficientFundsException.cs" -Force

# Data
New-Item -ItemType Directory -Path "$root\SimpleBankingCore.Data\Context" -Force
New-Item -ItemType Directory -Path "$root\SimpleBankingCore.Data\Repositories" -Force
New-Item -ItemType Directory -Path "$root\SimpleBankingCore.Data\Migrations" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Data\Context\BankingDbContext.cs" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Data\Repositories\IRepository.cs" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Data\Repositories\GenericRepository.cs" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Data\SimpleBankingCore.Data.csproj" -Force

# Services
New-Item -ItemType Directory -Path "$root\SimpleBankingCore.Services\Interfaces" -Force
New-Item -ItemType Directory -Path "$root\SimpleBankingCore.Services\Implementations" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Services\Interfaces\IAccountService.cs" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Services\Interfaces\ICustomerService.cs" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Services\Interfaces\ITransactionService.cs" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Services\Implementations\AccountService.cs" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Services\Implementations\CustomerService.cs" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Services\Implementations\TransactionService.cs" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Services\SimpleBankingCore.Services.csproj" -Force

# App
New-Item -ItemType Directory -Path "$root\SimpleBankingCore.App" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.App\Program.cs" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.App\appsettings.json" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.App\SimpleBankingCore.App.csproj" -Force

# Tests
New-Item -ItemType Directory -Path "$root\SimpleBankingCore.Tests\ServicesTests" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.Tests\SimpleBankingCore.Tests.csproj" -Force

# Root files
New-Item -ItemType File -Path "$root\.gitignore" -Force
New-Item -ItemType File -Path "$root\SimpleBankingCore.sln" -Force
