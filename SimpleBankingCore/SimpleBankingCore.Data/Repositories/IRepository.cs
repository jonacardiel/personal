#nullable enable
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Linq.Expressions;

namespace SimpleBankingCore.Data.Repositories
{
    // Generic interface for common database operations
    public interface IRepository<T> where T : class
    {
        Task<T?> GetByIdAsync(int id);
        Task<IEnumerable<T>> GetAllAsync();
        Task AddAsync(T entity);
        Task UpdateAsync(T entity);
        Task DeleteAsync(int id);
        Task<int> SaveChangesAsync(); // For committing changes to the database

        // New methods for flexible querying
        Task<T?> GetSingleOrDefaultAsync(Expression<System.Func<T, bool>> predicate, params Expression<System.Func<T, object>>[] includes);
        Task<IEnumerable<T>> FindAsync(Expression<System.Func<T, bool>> predicate);
    }
}
